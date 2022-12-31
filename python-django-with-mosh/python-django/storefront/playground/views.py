from gc import collect
from django.db import connection, transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from django.db.models import Q, F, Count, DecimalField, ExpressionWrapper, Func, Value
from django.db.models.aggregates import Max, Min, Avg, Sum
from django.db.models.functions import Concat
from store.models import Collection, Product, OrderItem, Order, Customer
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from .tasks import notify_customers


def say_hello(request):
    notify_customers.delay("Hello")
    return render(request, "hello.html", {"name": "Hanka"})
