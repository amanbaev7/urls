from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify


class BaseModel(models.Model):
    """
    Абстрактная базовая модель.

    Добавляет:
    - created_at — дата создания записи
    - updated_at — дата последнего обновления

    Используется для всех моделей, чтобы не дублировать код.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        abstract = True


class CompanyInfo(BaseModel):
    """
    Информация о компании (Singleton модель).

    В базе должна существовать только одна запись.
    Используется для:
    - верхней панели сайта
    - контактов
    - соцсетей
    - счетчика просмотров
    """

    work_hours = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Режим работы"
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Адрес"
    )

    instagram_url = models.URLField(
        blank=True,
        verbose_name="Instagram ссылка"
    )

    facebook_url = models.URLField(
        blank=True,
        verbose_name="Facebook ссылка"
    )

    map_url = models.URLField(
        blank=True,
        verbose_name="Ссылка на карту"
    )

    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

    def clean(self):
        """
        Валидация singleton.

        Запрещает создание более одной записи.
        Работает на уровне Django (не БД).
        """
        if not self.pk and CompanyInfo.objects.exists():
            raise ValidationError("Может существовать только одна запись CompanyInfo")

    def save(self, *args, **kwargs):
        """
        Перед сохранением вызывается валидация.
        """
        self.full_clean()
        return super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """
        Получение единственной записи.

        Если записи нет — создается автоматически.
        """
        obj, _ = cls.objects.get_or_create()
        return obj

    def __str__(self):
        return "Информация о компании"


class Page(BaseModel):
    """
    Страницы сайта (навигация).
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Название страницы"
    )

    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name="Slug (URL)"
    )

    content = models.TextField(
        blank=True,
        verbose_name="Контент страницы"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        constraints = [
            models.UniqueConstraint(
                fields=["order"],
                name="unique_page_order"
            )
        ]

    def save(self, *args, **kwargs):
        """
        Автоматическая генерация slug из title,
        если slug не указан.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Program(BaseModel):
    """
    Программы обучения или услуги.
    """

    name = models.CharField(
        max_length=200,
        verbose_name="Название программы"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )

    image = models.ImageField(
        upload_to="programs/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
        verbose_name="Изображение"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

    def __str__(self):
        return self.name


class Specialist(BaseModel):
    """
    Сотрудники / специалисты.
    """

    full_name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="ФИО"
    )

    position = models.CharField(
        max_length=200,
        verbose_name="Должность"
    )

    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="specialists",
        verbose_name="Программа"
    )

    photo = models.ImageField(
        upload_to="specialists/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
        verbose_name="Фотография"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"

    def __str__(self):
        return self.full_name