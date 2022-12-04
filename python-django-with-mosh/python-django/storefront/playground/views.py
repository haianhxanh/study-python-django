from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product, OrderItem, Order
from django.views.generic import TemplateView
    
def say_hello(request):
    queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    result = Product.objects.aggregate(Count('id'))

    return render(request, 'hello.html', {'name': 'Hanka', 'products': list(queryset), 'result': result})