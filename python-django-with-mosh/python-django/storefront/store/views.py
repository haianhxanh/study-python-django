import django.contrib
from django.core import serializers

# from django.core.cache import DefaultCacheProxy
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .pagination import DefaultPagination
from .models import Collection, Order, OrderItem, Product, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # specify fields used for filtering
    filterset_fields = ["collection_id", "unit_price"]
    # filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        # avoid retrieving instance 2x, this way, we only filter instances that exist in orders
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {"error": "Product cannot be deleted"},  # proper error message
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("product")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {"error": "Collection cannot be deleded"},  # proper error message
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
