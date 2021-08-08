from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

"""JWT auth"""
schema_view = get_schema_view(
    openapi.Info(
        title="Booking API",
        default_version="v1",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("meetings.urls")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
