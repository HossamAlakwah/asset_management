from django.urls import path

from .registry import router
from .schema import SchemaView
from .stats import StatsView

urlpatterns = [
    path("schema/", SchemaView.as_view(), name="ui-schema"),
    path("stats/", StatsView.as_view(), name="ui-stats"),
    *router.urls,
]
