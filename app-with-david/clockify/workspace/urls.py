from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.Register.as_view(), name="register"),
    path("api/users", views.ListAllUsers.as_view(), name="list-users"),
    path("api/tracking", views.ListTimeRecords.as_view(), name="list-time-records"),
    path("api/tracking/start", views.TrackingStart.as_view(), name="tracker-start"),
    path("api/tracking/stop", views.TrackingStop.as_view(), name="tracker-stop"),
]
