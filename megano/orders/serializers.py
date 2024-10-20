import datetime

from rest_framework import serializers
from orders.models import Order
from products.models import Product
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализация заказа
    """
    products = ProductSerializer(many=True)
    fullName = serializers.StringRelatedField()
    email = serializers.StringRelatedField()
    phone = serializers.StringRelatedField()
    createdAt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_createdAt(self, instance):
        date = instance.createdAt + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')

    def create(self, validated_data):
        products_tmp = (validated_data.pop('products'))
        products_id = [dict(product).get('id') for product in products_tmp]
        products = Product.objects.filter(pk__in=products_id)
        for product in products:
            print(product)
        order = Order.objects.create(**validated_data)
        order.products.set(products)
        return order

    def update(self, instance, validated_data):
        products_id = [dict(product).get('id') for product in validated_data.get('products')]
        products = Product.objects.filter(pk__in=products_id)
        instance.city = validated_data.get('city')
        instance.address = validated_data.get('address')
        instance.deliveryType = validated_data.get('deliveryType')
        instance.paymentType = validated_data.get('paymentType')
        instance.status = validated_data.get('status')
        instance.products.set(products)
        instance.save()
        return instance
