from rest_framework import serializers

from .models import CompanyInfo, Page, Program, Specialist

"""
DRF Serializers для преобразования моделей в JSON.

Все сериализаторы сделаны через `ModelSerializer`, чтобы они автоматически
соответствовали полям моделей.
"""


class CompanyInfoSerializer(serializers.ModelSerializer):
    # Верхняя панель: отдаем только нужные для фронтенда поля.
    class Meta:
        model = CompanyInfo
        fields = ("work_hours", "address", "instagram_url", "facebook_url", "views_count")


class PageNavigationSerializer(serializers.ModelSerializer):
    # Список страниц для кнопок навигации: только title + slug.
    class Meta:
        model = Page
        fields = ("title", "slug")


class PageDetailSerializer(serializers.ModelSerializer):
    # Детальная страница: полный контент и порядок.
    class Meta:
        model = Page
        fields = ("title", "slug", "content", "order")


class ProgramSerializer(serializers.ModelSerializer):
    # Программы/услуги (включая картинку).
    class Meta:
        model = Program
        fields = ("id", "name", "description", "image")


class SpecialistSerializer(serializers.ModelSerializer):
    # Список специалистов (включая фотографию).
    class Meta:
        model = Specialist
        fields = ("id", "full_name", "position", "photo")

