from django.contrib import admin
from catalog.models import Category
from products.models import Product, ProductImage, Tag, Specification, ProductSpecification, Sale


class ProductImages(admin.TabularInline):
    """
    Связываем изображения с продуктами
    """
    model = ProductImage


class ProductSpecifications(admin.TabularInline):
    """
    Связываем характеристики с продуктами
    """
    model = ProductSpecification

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Получение полей формы для внешнего ключа связи
        """
        if db_field.name == "name":
            pk_product = str(request).split('/')[4]
            product = Product.objects.get(pk=pk_product)
            specifications = Specification.objects.filter(category=product.category)
            kwargs["queryset"] = specifications
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Отображение продуктов в административной панели
    """
    list_display = [
        'pk',
        'title',
        'price',
        'count',
        'category',
        'limited_edition',
        'active'
    ]
    list_display_links = ['pk', 'title']
    inlines = [ProductImages, ProductSpecifications]
    list_filter = ['active', 'limited_edition', 'freeDelivery', 'rating']
    search_fields = ['title', 'category', 'price']
    actions = ['make_active', 'make_inactive']
    fieldsets = (
        ('О продукте', {
            'fields': ('category', 'title', ('price', 'count', 'rating'))
        }),
        ('Дополнительные параметры', {
            'classes': ('collapse',),
            'fields': ('limited_edition', 'freeDelivery', 'active')
        }),
        ('Описание товара', {
            'classes': ('collapse',),
            'fields': ('fullDescription',),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Получение полей формы для внешнего ключа связи
        """
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(parent__gte=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.action(description='Отметить, как активный продукт')
    def make_active(self, request, product):
        """
        Действие для установки категории активной
        :param request: запрос
        :param product: категория
        """
        updated = product.update(active=True)
        self.message_user(request, message=f'Продуктов отмечено АКТИВНЫМИ: {updated}')

    @admin.action(description='Отметить, как неактивный продукт')
    def make_inactive(self, request, product):
        """
        Действие для установки категории НЕ активной
        :param request: запрос
        :param product: категория
        """
        updated = product.update(active=False)
        self.message_user(request, message=f'Продуктов отмечено НЕАКТИВНЫМИ: {updated}')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Отображение в административной панели изображений продуктов
    """
    list_display = ['pk', 'product']
    list_display_links = ['pk', 'product']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Отображение тегов в административной панели
    """
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


class CategoryOfSpecification(admin.TabularInline):
    """
    Связываем характеристики продуктов с категорией
    """
    model = Specification.category.through


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """
    Отображение в административной панели характеристик продуктов
    """
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']
    inlines = [CategoryOfSpecification]
    exclude = ['category']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Отображение в административной панели продуктов, участвующих в распродаже
    """
    list_display = ['pk', 'product', 'price', 'salePrice']
    list_display_links = ['pk', 'product']
