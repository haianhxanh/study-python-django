import django.contrib
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import gc
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, OrderItem, Product
from .serializers import CollectionSerializer, ProductSerializer


class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)  # convert into dictionary
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            product, data=request.data
        )  # passing the instance here so the product will be updated
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(
                {"error": "Product cannot be deleted"},  # proper error message
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def product_detail(request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     if request.method == "GET":
    #         serializer = ProductSerializer(product)  # convert into dictionary
    #         return Response(serializer.data)
    #     elif request.method == "PUT":
    #         serializer = ProductSerializer(
    #             product, data=request.data
    #         )  # passing the instance here so the product will be updated
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     elif request.method == "DELETE":
    #         if product.orderitems.count() > 0:
    #             return Response(
    #                 {"error": "Product cannot be deleted"},  # proper error message
    #                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
    #             )
    #         product.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionDetail(APIView):
    def get(self, request, id):
        collection = get_object_or_404(Collection, pk=id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)


# @api_view()
# def collection_detail(request, pk):
#     return Response("ok")
