import collections
from black.brackets import max_delimiter_priority_in_atom
from django.db.models import Count
from rest_framework import serializers
import rest_framework.decorators
from store.models import Product, Collection
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "inventory",
            "description",
            "unit_price",
            "price_with_tax",
            "collection",
        ]

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name="CollectionDetail"
    # )

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        return product
