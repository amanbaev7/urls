from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

"""
Настройки Django Admin для моделей контента.

Важно:
- `CompanyInfo` — singleton, поэтому добавление второй записи запрещаем.
- `Page.content` редактируется через визуальный Summernote редактор.
"""

from .models import CompanyInfo, Page, Program, Specialist


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    # Какие поля отображать в списке.
    list_display = ("work_hours", "address", "views_count")
    # Какие поля показывать/редактировать на форме.
    fields = ("work_hours", "address", "instagram_url", "facebook_url", "views_count")

    def has_add_permission(self, request):
        # Singleton: добавлять можно только если запись еще не создана.
        return not CompanyInfo.objects.exists()


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    # SummernoteModelAdmin использует Summernote для полей контента.
    list_display = ("title", "slug", "order")
    # Автозаполнение slug из title в админке.
    prepopulated_fields = {"slug": ("title",)}
    # Поля, которые будут редактироваться через Summernote.
    summernote_fields = ("content",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    # В списке показываем название и id (id удобно, чтобы отличать элементы).
    list_display = ("name", "id")


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    # В списке показываем ФИО и должность.
    list_display = ("full_name", "position", "id")
