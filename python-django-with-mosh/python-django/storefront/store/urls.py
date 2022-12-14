from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from store.views import CartViewSet
from . import views
from pprint import pprint

# parent router
router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet, basename="carts")
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")

# creating child routers
# 1st param: parent router, 2nd param: parent prefix, 3rd param: lookup param
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")

# register child resource
# 1st arg: specify prefix, 2nd: ViewSet, 3rd: basename for generating URL patterns
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

products_router.register("images", views.ProductImageViewSet, basename="product-images")

carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
carts_router.register("items", views.CartItemViewSet, basename="cart-items")


# Compbine parent and child urls
urlpatterns = router.urls + products_router.urls + carts_router.urls
