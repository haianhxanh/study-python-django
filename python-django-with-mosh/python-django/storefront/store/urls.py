from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views
from pprint import pprint

# router = SimpleRouter()
router = DefaultRouter()
# 1st arg: endpoint, 2nd arg.: endpoint
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)
router.urls
# pprint(router.urls)

# Django default URL patterns
urlpatterns = router.urls

# custom URL patterns
# urlpatterns = [
#     path("test/", include(router.urls)),
# ]
