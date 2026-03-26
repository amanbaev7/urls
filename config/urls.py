from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

"""
Глобальные маршруты проекта.

Отвечает за:
- admin
- API
- сторонние приложения (summernote)
- media (только в DEBUG)
"""

urlpatterns = [
    # =========================
    # Admin
    # =========================
    path("admin/", admin.site.urls),

    # =========================
    # Summernote (редактор)
    # =========================
    path("summernote/", include("django_summernote.urls")),

    # =========================
    # API (versioned + namespaced)
    # =========================
    path(
        "api/v1/",
        include(("content.api_urls", "content"), namespace="content")
    ),
]


# =========================
# MEDIA (только для разработки)
# =========================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )