from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product, Reviews, Sale
from products.serializers import ProductSerializer, ReviewSerializer, SaleSerializer


class ProductPopularView(APIView):
    """
    Представление для отображения популярных продуктов
    """

    def get(self, request):
        products = Product.objects.filter(active=True).order_by('-rating')[:8].prefetch_related('images')
        for product in products:
            product.categoryName = product.category
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(viewsets.ViewSet):
    """
    Представление для отображения детальной страницы продукта
    """

    def retrieve(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)


class ProductLimitedView(APIView):
    """
    Представление для отображения лимитированных продуктов
    """

    def get(self, request):
        products = Product.objects.filter(limited_edition=True, active=True)[:15].prefetch_related('images')
        for product in products:
            product.categoryName = product.category
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class CreateReviewView(CreateModelMixin, GenericAPIView):
    """
    Представление для создания отзывов о продукте
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        pk = kwargs['pk']
        request.data['product'] = pk
        request.data['date'] = datetime.now()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        reviews = Reviews.objects.filter(product=pk)
        serializer = self.serializer_class(reviews, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SaleView(APIView):
    """
    Представление для отображения товаров со скидками
    """

    def get(self, request, *args, **kwargs):
        count_products_on_page = 8
        products = (Sale.objects.filter(Q(dateFrom__gte=datetime.today()) | Q(dateTo__gte=datetime.today())).
                    select_related('product').filter(product__active=True))
        paginator = Paginator(products, 8)
        current_page = paginator.get_page(request.GET.get('page'))
        if len(products) % count_products_on_page == 0:
            lastPage = len(products) // count_products_on_page
        else:
            lastPage = len(products) // count_products_on_page + 1
        serializer = SaleSerializer(current_page, many=True)
        return Response({'salesCards': serializer.data, 'currentPage': request.GET.get('page'), 'lastPage': lastPage})
