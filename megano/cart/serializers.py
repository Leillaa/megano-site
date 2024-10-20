from decimal import Decimal

from rest_framework import serializers

from products.models import Product


class BasketSerializer(serializers.ModelSerializer):
    """
    Сериализация корзины продуктов
    """
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = serializers.StringRelatedField(many=True)
    href = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_count(self, obj):
        return self.context.get(str(obj.pk)).get('count')

    def get_price(self, obj):
        return Decimal(self.context.get(str(obj.pk)).get('price'))
