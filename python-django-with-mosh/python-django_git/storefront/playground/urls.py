from importlib.resources import path
from django.urls import path
from . import views 
# import views from this folder in order to create reference

# URLConf
urlpatterns = [
  # on this URL playground/hello (playground is not mentioned because it was configured in urls.py in the main app already), we refer to function say_hello created earlier in views.py
  # always end URL with /
  path('hello/', views.say_hello) 
]