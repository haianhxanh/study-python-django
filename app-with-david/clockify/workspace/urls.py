from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register/', views.register, name='register'),
  path("api/users", views.ListAllUsers.as_view(), name="list-users"),
  path("api/tracking/start", views.TrackingStart.as_view(), name="tracker-start")
]