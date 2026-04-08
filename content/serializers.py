from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import CompanyInfo, Page, Program, Specialist


# =========================
# CompanyInfo
# =========================

class CompanyInfoReadSerializer(serializers.ModelSerializer):
    """
    Чтение информации о компании.

    Используется для фронтенда (верхняя панель).
    Поле views_count только для чтения.
    """

    class Meta:
        model = CompanyInfo
        fields = (
            "work_hours",
            "address",
            "instagram_url",
            "facebook_url",
            "map_url",
            "views_count",
        )
        read_only_fields = ("views_count",)


class CompanyInfoWriteSerializer(serializers.ModelSerializer):
    """
    Запись информации о компании.

    Ограничивает изменение счетчика просмотров.
    Добавляет базовую валидацию URL.
    """

    class Meta:
        model = CompanyInfo
        fields = (
            "work_hours",
            "address",
            "instagram_url",
            "facebook_url",
            "map_url",
        )

    def validate(self, attrs):
        """
        Дополнительная проверка URL.
        """
        validator = URLValidator()

        for field in ["instagram_url", "facebook_url", "map_url"]:
            value = attrs.get(field)
            if value:
                try:
                    validator(value)
                except DjangoValidationError:
                    raise serializers.ValidationError({field: "Некорректный URL"})

        return attrs


# =========================
# Page
# =========================

class PageNavigationSerializer(serializers.ModelSerializer):
    """
    Навигация (меню).

    Минимальный набор данных для кнопок.
    """

    class Meta:
        model = Page
        fields = ("title", "slug")


class PageDetailSerializer(serializers.ModelSerializer):
    """
    Детальная страница.
    """

    class Meta:
        model = Page
        fields = ("title", "slug", "content", "order")


class PageWriteSerializer(serializers.ModelSerializer):
    """
    Создание/редактирование страниц.

    Добавляет валидацию title и order.
    """

    class Meta:
        model = Page
        fields = ("title", "slug", "content", "order")

    def validate_title(self, value):
        """
        Минимальная длина названия.
        """
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Название слишком короткое")
        return value

    def validate_order(self, value):
        """
        Проверка на отрицательные значения.
        """
        if value < 0:
            raise serializers.ValidationError("Порядок не может быть отрицательным")
        return value


# =========================
# Program
# =========================

class ProgramReadSerializer(serializers.ModelSerializer):
    """
    Чтение программ.

    Добавляет абсолютный URL изображения.
    """

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ("id", "name", "description", "image", "image_url")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProgramWriteSerializer(serializers.ModelSerializer):
    """
    Создание/редактирование программ.

    Добавляет валидацию имени.
    """

    class Meta:
        model = Program
        fields = ("name", "description", "image")

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название слишком короткое")
        return value


# =========================
# Specialist
# =========================

class SpecialistReadSerializer(serializers.ModelSerializer):
    """
    Чтение специалистов.

    Включает:
    - название программы
    - URL фотографии
    """

    program_name = serializers.CharField(
        source="program.name",
        read_only=True
    )

    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = (
            "id",
            "full_name",
            "position",
            "program",
            "program_name",
            "photo",
            "photo_url",
        )

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None


class SpecialistWriteSerializer(serializers.ModelSerializer):
    """
    Создание/редактирование специалистов.

    Добавляет валидацию ФИО.
    """

    class Meta:
        model = Specialist
        fields = ("full_name", "position", "program", "photo")

    def validate_full_name(self, value):
        if len(value.strip().split()) < 2:
            raise serializers.ValidationError("Укажите имя и фамилию")
        return value