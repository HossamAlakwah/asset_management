"""Inventory counts for the web dashboard."""

from django.db.models import Count
from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from assets.models import NotificationConfig

from .registry import registered_resources


@extend_schema(
    tags=["Meta"],
    summary="Dashboard totals",
    description="Per-resource record counts, including a status breakdown when the model has a status field.",
    responses={200: OpenApiTypes.OBJECT},
)
class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cards = []
        for prefix, viewset in registered_resources():
            if prefix == "users" and not request.user.is_super_admin():
                continue
            if getattr(viewset, "ui_hidden", False):
                continue
            queryset = getattr(viewset, "queryset", None)
            if queryset is None:
                continue
            model = queryset.model
            item = {
                "key": prefix,
                "title": getattr(viewset, "ui_title", prefix),
                "group": getattr(viewset, "ui_group", "Other"),
                "icon": getattr(viewset, "ui_icon", "box"),
                "total": queryset.count(),
                "by_status": {},
            }
            if any(field.name == "status" for field in model._meta.fields):
                rows = queryset.values("status").annotate(total=Count("id"))
                item["by_status"] = {
                    (row["status"] or "Unset"): row["total"] for row in rows
                }
                if hasattr(model, "Status") and hasattr(model.Status, "STOCK"):
                    item["in_stock"] = queryset.filter(status=model.Status.STOCK).count()
            cards.append(item)
        return Response(
            {
                "cards": cards,
                "alerts": {
                    "total": NotificationConfig.objects.count(),
                    "active": NotificationConfig.objects.filter(is_active=True).count(),
                },
            }
        )
