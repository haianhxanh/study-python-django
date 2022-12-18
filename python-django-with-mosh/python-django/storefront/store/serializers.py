import collections
from black.brackets import max_delimiter_priority_in_atom
from django.db.models import Count
from rest_framework import serializers
import rest_framework.decorators
from store.models import Cart, CartItem, Product, Collection, Review
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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()  # to show product with more details
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        # list comprehension
        return sum(
            [item.quantity * item.product.unit_price for item in cart.items.all()]
        )

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = (
        serializers.IntegerField()
    )  # we have to define this field because it's dynamically generated

    # validate input
    # convention validate_FIELD_NAME()
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with given ID")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:  # update an existing item
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:  # add new item
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]
