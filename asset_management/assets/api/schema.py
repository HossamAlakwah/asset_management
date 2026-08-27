"""Describes every resource so the web UI can build itself from the API."""

from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from assets.models import NotificationConfig
from users.twofactor import two_factor_is_confirmed

from .excel import ExcelIOMixin
from .registry import model_to_prefix, registered_resources

HIDDEN_FIELDS = {"id", "logs"}

TEXTAREA_FIELDS = {
    "comment",
    "comments",
    "notification_message",
    "message",
}


def _describe_field(name, field, relations):
    info = {
        "name": name,
        "label": str(field.label) if field.label else name.replace("_", " ").title(),
        "required": bool(field.required) and not field.read_only,
        "read_only": bool(field.read_only),
        "help": str(field.help_text) if field.help_text else "",
        "type": "string",
    }

    if isinstance(field, serializers.ListSerializer):
        child = field.child
        info["type"] = "nested"
        info["fields"] = [
            _describe_field(child_name, child_field, relations)
            for child_name, child_field in child.fields.items()
            if child_name not in HIDDEN_FIELDS
        ]
        return info

    if isinstance(field, serializers.ManyRelatedField):
        info["type"] = "relation"
        info["many"] = True
        info["resource"] = relations.get(
            getattr(field.child_relation, "queryset", None).model
            if getattr(field.child_relation, "queryset", None) is not None
            else None
        )
        return info

    if isinstance(field, serializers.PrimaryKeyRelatedField):
        queryset = getattr(field, "queryset", None)
        info["type"] = "relation"
        info["many"] = False
        info["resource"] = relations.get(queryset.model) if queryset is not None else None
        return info

    if isinstance(field, serializers.ChoiceField):
        info["type"] = "choice"
        info["choices"] = [
            {"value": value, "label": str(label)}
            for value, label in field.choices.items()
        ]
        if "Stock" in field.choices:
            info["omit_on_create"] = True
            info["create_default"] = "Stock"
        return info

    if isinstance(field, serializers.BooleanField):
        info["type"] = "boolean"
    elif isinstance(field, serializers.IntegerField):
        info["type"] = "integer"
    elif isinstance(field, (serializers.FloatField, serializers.DecimalField)):
        info["type"] = "float"
    elif isinstance(field, serializers.DateTimeField):
        info["type"] = "datetime"
    elif isinstance(field, serializers.DateField):
        info["type"] = "date"
    elif isinstance(field, serializers.EmailField):
        info["type"] = "email"
    elif isinstance(field, serializers.CharField):
        info["type"] = "text" if name in TEXTAREA_FIELDS else "string"

    return info


def _serializer_instance(viewset):
    """Build a serializer even when the ViewSet only implements get_serializer_class."""
    view = viewset()
    view.action = "list"
    view.request = None
    view.format_kwarg = None
    serializer_class = getattr(view, "get_serializer_class", lambda: None)()
    if serializer_class is None:
        serializer_class = getattr(viewset, "serializer_class", None)
    if serializer_class is None:
        return None
    return serializer_class()


def _describe_resource(prefix, viewset, relations, request):
    serializer = _serializer_instance(viewset)
    if serializer is None:
        return None
    fields = [
        _describe_field(name, field, relations)
        for name, field in serializer.fields.items()
        if name not in HIDDEN_FIELDS
    ]

    list_fields = list(getattr(viewset, "ui_list_fields", []))
    if not list_fields:
        list_fields = [f["name"] for f in fields][:6]

    option_fields = list(getattr(viewset, "ui_option_fields", []))
    if not option_fields:
        option_fields = list_fields[:1]

    actions = []
    if hasattr(viewset, "unassign"):
        actions.append("unassign")

    return {
        "key": prefix,
        "title": getattr(viewset, "ui_title", prefix.replace("-", " ").title()),
        "group": getattr(viewset, "ui_group", "Other"),
        "icon": getattr(viewset, "ui_icon", "box"),
        "endpoint": f"/api/v1/{prefix}/",
        "fields": fields,
        "list_fields": list_fields,
        "option_fields": option_fields,
        "search_fields": list(getattr(viewset, "search_fields", [])),
        "filter_fields": list(getattr(viewset, "filterset_fields", [])),
        "ordering_fields": list(getattr(viewset, "ordering_fields", [])),
        "log_field": getattr(viewset, "ui_log_field", None),
        "supports_excel": issubclass(viewset, ExcelIOMixin),
        "read_only": not hasattr(viewset, "create"),
        "actions": actions,
    }


@extend_schema(
    tags=["Meta"],
    summary="UI resource schema",
    description=(
        "Describes every registered resource: its fields and types, choice "
        "values, relations, default list columns and whether it supports "
        "Excel import/export. The web UI builds its tables and forms from "
        "this document, so a new resource needs no front-end changes."
    ),
    responses={200: OpenApiTypes.OBJECT},
)
class SchemaView(APIView):
    """Machine-readable description of all resources, used to render the UI."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        relations = model_to_prefix()
        user = request.user
        resources = []
        for prefix, viewset in registered_resources():
            if prefix == "users" and not user.is_super_admin():
                continue
            if getattr(viewset, "ui_hidden", False):
                continue
            described = _describe_resource(prefix, viewset, relations, request)
            if described:
                resources.append(described)
        return Response(
            {
                "user": {
                    "username": user.username,
                    "full_name": user.get_full_name(),
                    "role": user.role,
                    "is_admin": user.is_admin(),
                    "is_super_admin": user.is_super_admin(),
                    "two_factor_enabled": two_factor_is_confirmed(user),
                },
                "resources": resources,
                "alerts": {
                    "endpoint": "/api/v1/notification-configs/",
                    "sent_endpoint": "/api/v1/sent-notifications/",
                    "models": [
                        {"value": value, "label": label}
                        for value, label in NotificationConfig.MODEL_CHOICES
                    ],
                },
            }
        )
