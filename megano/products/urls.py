from django.urls import path
from products.views import ProductPopularView, ProductDetailView, ProductLimitedView, CreateReviewView, SaleView

app_name = 'products'

urlpatterns = [
    path("api/products/popular/", ProductPopularView.as_view()),
    path("api/products/limited/", ProductLimitedView.as_view()),
    path("api/product/<int:pk>/", ProductDetailView.as_view({'get': 'retrieve'})),
    path("api/product/<int:pk>/review/", CreateReviewView.as_view()),
    path("api/sales/", SaleView.as_view()),
]
