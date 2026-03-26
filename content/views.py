from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CompanyInfo, Page, Program, Specialist
from .serializers import (
    CompanyInfoSerializer,
    PageDetailSerializer,
    PageNavigationSerializer,
    ProgramSerializer,
    SpecialistSerializer,
)

"""
Представления (views) приложения `content`.

Здесь реализованы REST endpoint'ы, которые возвращают контент сайта в формате JSON:
- режим работы/адрес/соцсети (singleton CompanyInfo)
- список страниц и контент страниц по `slug`
- список программ и специалистов
- POST для инкремента счетчика просмотров главной страницы
"""


class CommonInfoView(APIView):
    # Доступ разрешен всем (без авторизации), т.к. это публичный сайт.
    permission_classes = [AllowAny]

    def get(self, request):
        # Получаем singleton-запись. Если ее нет — она создается автоматически.
        company = CompanyInfo.get_solo()
        # Передаем `request` в контекст сериализатора, чтобы ImageField отдал корректные URL.
        return Response(CompanyInfoSerializer(company, context={"request": request}).data)


class PagesListView(APIView):
    # Публичный список навигационных страниц.
    permission_classes = [AllowAny]

    def get(self, request):
        # Даем список в нужном порядке: сначала `order`, затем стабильность по `id`.
        qs = Page.objects.all().order_by("order", "id")
        return Response(PageNavigationSerializer(qs, many=True, context={"request": request}).data)


class PageDetailView(APIView):
    # Публичный endpoint конкретной страницы по `slug`.
    permission_classes = [AllowAny]

    def get(self, request, slug: str):
        # Ищем страницу именно по slug (как требуется ТЗ).
        page = get_object_or_404(Page, slug=slug)
        return Response(PageDetailSerializer(page, context={"request": request}).data)


class ProgramsListView(APIView):
    # Публичный список программ.
    permission_classes = [AllowAny]

    def get(self, request):
        # Сортировка по id для предсказуемого вывода.
        qs = Program.objects.all().order_by("id")
        return Response(ProgramSerializer(qs, many=True, context={"request": request}).data)


class SpecialistsListView(APIView):
    # Публичный список специалистов.
    permission_classes = [AllowAny]

    def get(self, request):
        # Сортировка по id для предсказуемого вывода.
        qs = Specialist.objects.all().order_by("id")
        return Response(SpecialistSerializer(qs, many=True, context={"request": request}).data)


class IncrementViewsView(APIView):
    """
    POST /api/v1/increment-views/
    Инкрементирует views_count на +1 (используется для главной страницы).
    """

    # Открытый endpoint; при желании можно позже добавить защиту (rate limit/auth).
    permission_classes = [AllowAny]

    def post(self, request):
        # Гарантируем наличие singleton-записи до обновления.
        CompanyInfo.get_solo()
        # Обновляем счетчик на уровне БД через F-expression (меньше гонок при параллельных запросах).
        CompanyInfo.objects.filter(pk=1).update(views_count=F("views_count") + 1)
        # Возвращаем актуальное значение после обновления.
        company = CompanyInfo.get_solo()
        return Response({"views_count": company.views_count})
