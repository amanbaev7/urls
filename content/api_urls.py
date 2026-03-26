from django.urls import path

from .views import (
    CommonInfoView,
    IncrementViewsView,
    PageDetailView,
    PagesListView,
    ProgramsListView,
    SpecialistsListView,
)

# Набор маршрутов для REST API контента сайта.
urlpatterns = [
    # GET /api/v1/common-info/
    path("common-info/", CommonInfoView.as_view(), name="common-info"),
    # GET /api/v1/pages/
    path("pages/", PagesListView.as_view(), name="pages-list"),
    # GET /api/v1/pages/{slug}/
    path("pages/<slug:slug>/", PageDetailView.as_view(), name="pages-detail"),
    # GET /api/v1/programs/
    path("programs/", ProgramsListView.as_view(), name="programs-list"),
    # GET /api/v1/specialists/
    path("specialists/", SpecialistsListView.as_view(), name="specialists-list"),
    # POST /api/v1/increment-views/
    path("increment-views/", IncrementViewsView.as_view(), name="increment-views"),
]

