from django.db.models import F
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from .models import CompanyInfo, Page, Program, Specialist
from .serializers import (
    CompanyInfoReadSerializer,
    PageNavigationSerializer,
    PageDetailSerializer,
    ProgramReadSerializer,
    SpecialistReadSerializer,
)


# =========================
# CompanyInfo (Singleton)
# =========================

class CompanyInfoViewSet(ReadOnlyModelViewSet):
    """
    Singleton API для информации о компании.

    list() возвращает единственную запись.
    """

    serializer_class = CompanyInfoReadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Всегда возвращает один объект.
        """
        return CompanyInfo.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Переопределяем list → возвращаем singleton.
        """
        company = CompanyInfo.get_solo()
        serializer = self.get_serializer(company)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def increment_views(self, request):
        """
        POST /company-info/increment_views/

        Безопасный инкремент счетчика.
        """

        company = CompanyInfo.get_solo()

        CompanyInfo.objects.filter(pk=company.pk).update(
            views_count=F("views_count") + 1
        )

        company.refresh_from_db()

        return Response({
            "views_count": company.views_count
        })


# =========================
# Page
# =========================

class PageViewSet(ReadOnlyModelViewSet):
    """
    API страниц.

    list → навигация  
    retrieve → детальная страница  
    """

    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Page.objects.all().order_by("order", "id")

    def get_serializer_class(self):
        """
        Разные сериализаторы:
        - list → легкий
        - retrieve → полный
        """
        if self.action == "list":
            return PageNavigationSerializer
        return PageDetailSerializer


# =========================
# Program
# =========================

class ProgramViewSet(ReadOnlyModelViewSet):
    """
    API программ.
    """

    permission_classes = [AllowAny]
    serializer_class = ProgramReadSerializer

    def get_queryset(self):
        return Program.objects.all().order_by("id")


# =========================
# Specialist
# =========================

class SpecialistViewSet(ReadOnlyModelViewSet):
    """
    API специалистов.

    Оптимизирован select_related.
    """

    permission_classes = [AllowAny]
    serializer_class = SpecialistReadSerializer

    def get_queryset(self):
        return Specialist.objects.select_related("program").all().order_by("id")