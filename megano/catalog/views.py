import random

from django.core.paginator import Paginator
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Category
from catalog.serializers import CategorySerializer, TagsSerializer, BannersSerializer
from products.models import Tag, Product
from products.serializers import ProductSerializer


class CategoryView(APIView):
    """
    Представление для получения категорий товаров
    """

    def get(self, request):
        categories = []
        categories_tmp = Category.objects.filter(parent=None, active=True).prefetch_related('image', 'subcategories')
        for category in categories_tmp:
            subcategories = [subcategory for subcategory in category.subcategories.filter(active=True)]
            categories.append({'id': category.id, 'title': category.title, 'subcategories': subcategories,
                               'href': category.href, 'image': category.image})
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class TagsView(APIView):
    """
    Представление для получения тэгов товаров
    """

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data)


class BannersView(APIView):
    """
    Представление для получения баннеров главной страницы
    """

    def get(self, request):
        categories = []
        categories_tmp = Category.objects.filter(parent__isnull=False, active=True, favourite=True).prefetch_related(
            'products')
        if len(categories_tmp) > 3:
            categories_tmp = random.sample(list(categories_tmp), 3)
        for category in categories_tmp:
            product = category.products.order_by('price').first()
            product_min_price = product.price
            product_image = product.images
            categories.append({'href': category.href, 'title': category.title, 'price': product_min_price,
                               'images': product_image})
        serializer = BannersSerializer(categories, many=True)
        return Response({'banners': serializer.data})


def sorting_catalog(request, products):
    """
    Сортировка каталога по входящим параметрам
    :param products: продукты
    :param request: запрос
    :return: продукты в соответствии с сортировкой
    """
    sort = request.GET.get('sort')
    sortType = request.GET.get('sortType')
    if sortType == 'inc':
        sortType = '-'
    else:
        sortType = ''
    if sort == 'reviews':
        products = products.filter(active=True).annotate(count_reviews=Count('reviews')).order_by(
            f'{sortType}count_reviews'). \
            prefetch_related('images', 'reviews')
    else:
        products = products.filter(active=True).order_by(f'{sortType}{sort}').prefetch_related('images', 'reviews')
    return products


def filter_catalog(request):
    """
    Фильтрация каталога по входящим параметрам
    :param request: запрос
    :return: продукты в соответствии с фильтрацией
    """
    category = request.query_params.get('category')
    title = request.query_params.get('filter[name]')
    available = request.query_params.get('filter[available]').capitalize()
    freeDelivery = request.query_params.get('filter[freeDelivery]').capitalize()
    tags = request.query_params.get('tags', '').split(',')
    search = request.query_params.get('filter[search]', '')
    min_price = (request.query_params.get('filter[minPrice]'))
    max_price = (request.GET.get('filter[maxPrice]'))
    if category != '0':
        catalog = Category.objects.get(pk=category, active=True).products
    else:
        catalog = Product.objects
    if available == 'True':
        if freeDelivery == 'True':
            if tags != ['']:
                catalog = (catalog.filter(
                        title__iregex=title, price__range=(min_price, max_price), count__gt=0, freeDelivery=True,
                        tags__in=tags).prefetch_related('images', 'tags'))
            else:
                catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), count__gt=0,
                                         freeDelivery=True).prefetch_related('images')
        elif tags != ['']:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), count__gt=0,
                                     tags__in=tags).prefetch_related('images', 'tags')
        elif search:
            catalog = catalog.filter(title__iregex=search, price__range=(min_price, max_price),
                                     count__gt=0).prefetch_related('images')
        else:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                     count__gt=0).prefetch_related('images')
    elif freeDelivery == 'True':
        if tags != ['']:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), freeDelivery=True,
                                     tags__in=tags).prefetch_related('images', 'tags')
        else:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                     freeDelivery=True).prefetch_related('images')
    elif tags != ['']:
        catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                 tags__in=tags).prefetch_related('images', 'tags')
    else:
        catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price)).prefetch_related('images')
    return catalog


class CatalogView(APIView):
    """
    Представление для получения товаров каталога
    """

    def get(self, request, *args, **kwargs):
        products = filter_catalog(request)
        products = sorting_catalog(request, products)
        paginator = Paginator(products, 8)
        current_page = paginator.get_page(request.GET.get('page'))
        if len(products) % 8 == 0:
            lastPage = len(products) // 8
        else:
            lastPage = len(products) // 8 + 1
        for product in current_page:
            product.categoryName = product.category
        serializer = ProductSerializer(current_page, many=True)
        return Response({'items': serializer.data, 'currentPage': request.GET.get('page'), 'lastPage': lastPage})
