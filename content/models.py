from django.db import models

"""
Модели приложения `content`.

Здесь описана структура данных для информационной панели:
- `CompanyInfo` хранит верхнюю панель сайта и работает как singleton (одна запись в БД).
- `Page` — страницы для кнопок навигации, контент которых редактируется в admin.
- `Program` и `Specialist` — справочные данные для соответствующих разделов.
"""


class CompanyInfo(models.Model):
    """
    Singleton-model: в базе должна существовать только одна запись.
    Используется для верхней панели (режим работы, адрес, соцсети, счетчик просмотров).
    """

    # Режим работы (например: "Пн-Пт 07:00-18:00")
    work_hours = models.CharField(max_length=200, blank=True)
    # Адрес организации (например: "с. Араван ул. Ленина 94")
    address = models.CharField(max_length=255, blank=True)
    # Соцсети — URL поля. Пустые значения разрешены, чтобы можно было заполнять постепенно.
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    # Счетчик просмотров главной страницы.
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Company info"
        verbose_name_plural = "Company info"

    def save(self, *args, **kwargs):
        # Принудительно фиксируем PK, чтобы в таблице гарантированно была одна строка.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls) -> "CompanyInfo":
        # Получаем запись singleton. Если ее еще нет — создаем автоматически.
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        # Удобочитаемое представление в админке.
        return "Company info (singleton)"


class Page(models.Model):
    """
    Страницы для кнопок навигации/разделов сайта.
    """

    # Заголовок кнопки/раздела (например, "О нас")
    title = models.CharField(max_length=200)
    # Уникальный slug для URL (например, "about", "admissions")
    slug = models.SlugField(unique=True)
    # HTML/Markdown контент (Summernote в admin позволит редактировать визуально).
    content = models.TextField(blank=True)
    # Порядок сортировки в меню.
    order = models.PositiveIntegerField(default=0)

    class Meta:
        # Сортируем страницы сначала по `order`, затем стабильностью по `id`.
        ordering = ["order", "id"]

    def __str__(self):
        # Удобочитаемое представление в админке.
        return f"{self.title} ({self.slug})"


class Program(models.Model):
    """
    Программы обучения/услуги.
    """

    # Название программы
    name = models.CharField(max_length=200)
    # Описание (может быть HTML/текст — формат определяется тем, как вы будете его отображать во фронтенде)
    description = models.TextField(blank=True)
    # Картинка/иконка программы
    image = models.ImageField(upload_to="programs/", blank=True, null=True)

    class Meta:
        # Стабильная сортировка в API.
        ordering = ["id"]

    def __str__(self):
        # Удобочитаемое представление в админке.
        return self.name


class Specialist(models.Model):
    """
    Сотрудники/специалисты.
    """

    # ФИО
    full_name = models.CharField(max_length=200)
    # Должность
    position = models.CharField(max_length=200)
    # Фотография специалиста
    photo = models.ImageField(upload_to="specialists/", blank=True, null=True)

    class Meta:
        # Стабильная сортировка в API.
        ordering = ["id"]

    def __str__(self):
        # Удобочитаемое представление в админке.
        return f"{self.full_name} ({self.position})"
