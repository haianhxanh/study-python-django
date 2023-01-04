from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r"projects", views.ProjectViewSet, basename="projects")
task_router = routers.NestedDefaultRouter(router, r"projects", lookup="project")
task_router.register(r"tasks", views.TaskViewSet, basename="tasks")
project_user_router = routers.NestedDefaultRouter(router, r"projects", lookup="project")
project_user_router.register(r"users", views.UserProjectViewSet, basename="users")

router.register(r"users", views.UserViewSet, basename="users")
user_tracking_router = routers.NestedDefaultRouter(router, r"users", lookup="user")
user_tracking_router.register(r"tracking", views.TimeRecordViewSet, basename="tracking")

urlpatterns = [
    path("", views.home, name="home"),
    path("", include(router.urls)),
    path("", include(task_router.urls)),
    path("", include(project_user_router.urls)),
    path("", include(user_tracking_router.urls)),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("register/", views.Register.as_view(), name="register"),
    # path("users", views.ListAllUsers.as_view(), name="list-users"),
    # path("tracking", views.ListTimeRecords.as_view(), name="list-time-records"),
    path("tracking/start", views.TrackingStart.as_view(), name="tracker-start"),
    path("tracking/stop", views.TrackingStop.as_view(), name="tracker-stop"),
]
