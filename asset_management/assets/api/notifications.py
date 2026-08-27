from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.models import NotificationConfig, NotificationRecipient, SentNotification
from assets.utils.notifications import evaluate_config


class NotificationConfigSerializer(serializers.ModelSerializer):
    recipients = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True,
        help_text="Email addresses that receive this alert.",
    )
    subscriber_count = serializers.SerializerMethodField()

    class Meta:
        model = NotificationConfig
        fields = (
            "id",
            "model_name",
            "condition_type",
            "condition_value",
            "is_active",
            "notification_message",
            "recipients",
            "subscriber_count",
        )

    def get_subscriber_count(self, obj):
        return obj.subscribers.filter(is_active=True).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["recipients"] = list(
            instance.subscribers.filter(is_active=True)
            .order_by("email")
            .values_list("email", flat=True)
        )
        data["subscriber_count"] = len(data["recipients"])
        return data

    def create(self, validated_data):
        emails = validated_data.pop("recipients", [])
        with transaction.atomic():
            config = super().create(validated_data)
            self._sync_recipients(config, emails)
        return config

    def update(self, instance, validated_data):
        emails = validated_data.pop("recipients", None)
        with transaction.atomic():
            config = super().update(instance, validated_data)
            if emails is not None:
                self._sync_recipients(config, emails)
        return config

    def _sync_recipients(self, config, emails):
        recipients = []
        for email in emails:
            recipient, _created = NotificationRecipient.objects.get_or_create(
                email=email.strip().lower(),
                defaults={"is_active": True},
            )
            if not recipient.is_active:
                recipient.is_active = True
                recipient.save(update_fields=["is_active"])
            recipients.append(recipient)
        config.subscribers.set(recipients)


class NotificationRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationRecipient
        fields = ("id", "email", "is_active", "models_to_notify", "created_at")
        read_only_fields = ("id", "created_at")


class SentNotificationSerializer(serializers.ModelSerializer):
    recipient_email = serializers.CharField(source="recipient.email", read_only=True)
    config_label = serializers.SerializerMethodField()

    class Meta:
        model = SentNotification
        fields = (
            "id",
            "config",
            "config_label",
            "recipient",
            "recipient_email",
            "triggered_by",
            "message",
            "sent_at",
        )
        read_only_fields = fields

    def get_config_label(self, obj):
        return str(obj.config)


class NotificationConfigViewSet(viewsets.ModelViewSet):
    queryset = NotificationConfig.objects.all().prefetch_related("subscribers")
    serializer_class = NotificationConfigSerializer
    filterset_fields = ["model_name", "condition_type", "is_active"]
    search_fields = ["model_name", "condition_value", "notification_message"]
    ordering_fields = ["model_name", "condition_value"]

    ui_title = "Alert Rules"
    ui_group = "Notifications"
    ui_icon = "bell"
    ui_hidden = True
    ui_list_fields = [
        "model_name",
        "condition_type",
        "condition_value",
        "is_active",
    ]

    @extend_schema(summary="Run this alert now")
    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        config = self.get_object()
        result = evaluate_config(config, send=True)
        return Response(result)


class NotificationRecipientViewSet(viewsets.ModelViewSet):
    queryset = NotificationRecipient.objects.prefetch_related("models_to_notify")
    serializer_class = NotificationRecipientSerializer
    filterset_fields = ["is_active"]
    search_fields = ["email"]
    ordering_fields = ["email", "created_at"]

    ui_title = "Alert Recipients"
    ui_group = "Notifications"
    ui_icon = "mail"
    ui_hidden = True
    ui_list_fields = ["email", "is_active", "created_at"]


class SentNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SentNotification.objects.select_related("config", "recipient")
    serializer_class = SentNotificationSerializer
    filterset_fields = ["config", "recipient"]
    ordering_fields = ["sent_at"]
    ordering = ["-sent_at"]

    ui_title = "Sent Alerts"
    ui_group = "Notifications"
    ui_icon = "history"
    ui_hidden = True
    ui_list_fields = ["config", "recipient", "triggered_by", "sent_at"]
