from django.contrib import admin
from django.db.models import F
from django_summernote.admin import SummernoteModelAdmin

from .models import CompanyInfo, Page, Program, Specialist


# =========================
# CompanyInfo (Singleton)
# =========================

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("work_hours", "address", "views_count", "updated_at")

    readonly_fields = (
        "views_count",
        "created_at",
        "updated_at",
    )

    fields = (
        "work_hours",
        "address",
        "instagram_url",
        "facebook_url",
        "views_count",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        # Можно создать новую запись, только если нет ни одной
        return not CompanyInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # РАЗРЕШАЕМ удаление
        return True


# =========================
# Page
# =========================

@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    """
    Админка страниц с визуальным редактором.
    """

    list_display = ("title", "slug", "order", "created_at")
    list_editable = ("order",)
    search_fields = ("title", "slug")
    ordering = ("order", "id")

    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("content",)

    list_per_page = 20


# =========================
# Program
# =========================

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Админка программ.
    """

    list_display = ("name", "id", "created_at")
    search_fields = ("name",)
    ordering = ("id",)

    list_per_page = 20


# =========================
# Specialist
# =========================

@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    """
    Админка специалистов.
    """

    list_display = ("full_name", "position", "program", "id")
    search_fields = ("full_name", "position")
    list_filter = ("program",)

    autocomplete_fields = ("program",)

    ordering = ("id",)
    list_per_page = 20