from gc import collect
from django.db import connection, transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.db.models import Q, F, Count, DecimalField, ExpressionWrapper, Func, Value
from django.db.models.aggregates import Max, Min, Avg, Sum
from django.db.models.functions import Concat
from store.models import Collection, Product, OrderItem, Order, Customer
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem


def say_hello(request):
    try:
        # send_mail("subject", "message", "hankawork@gmail.com", ["hanka7n@gmail.com", "hankawork@gmail.com"])
        # mail_admins("subject", "message", html_message="message")
        message = EmailMessage(
            "subject", "message", "hankawork@gmail.com", ["hanka7n@gmail.com", "hankawork@gmail.com"]
        )
        message.attach_file("playground/static/images/blake-yuto-VqxNK0FpSPo-unsplash.jpg")
        message.send()
    except BadHeaderError:
        pass  # e.g. Email successfully sent
    return render(request, "hello.html", {"name": "Hanka"})
