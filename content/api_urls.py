from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CompanyInfoViewSet,
    PageViewSet,
    ProgramViewSet,
    SpecialistViewSet,
)

"""
Маршруты API (router-based).

ВАЖНО:
- здесь НЕ должно быть 'api/v1/'
- только router
"""

router = DefaultRouter()

# Singleton (CompanyInfo)
router.register(r"company", CompanyInfoViewSet, basename="company")

# Pages
router.register(r"pages", PageViewSet, basename="pages")

# Programs
router.register(r"programs", ProgramViewSet, basename="programs")

# Specialists
router.register(r"specialists", SpecialistViewSet, basename="specialists")


# ❗ КЛЮЧЕВАЯ ЧАСТЬ (у тебя её не было)
urlpatterns = [
    path("", include(router.urls)),
]