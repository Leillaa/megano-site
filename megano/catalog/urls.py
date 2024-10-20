from django.urls import path
from catalog.views import CategoryView, TagsView, BannersView, CatalogView

urlpatterns = [
    path("api/categories/", CategoryView.as_view()),
    path("api/banners/", BannersView.as_view()),
    path("api/tags/", TagsView.as_view()),
    path("api/catalog/", CatalogView.as_view()),
]
