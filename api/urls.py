from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (PurchaseViewSet, IngredientsViewSet, FollowViewSet,
                    FavoriteViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'ingredients', IngredientsViewSet, basename="ingredienst")
router_v1.register(r'subscriptions', FollowViewSet,
                   basename="subscriptions")
router_v1.register(r'favorites', FavoriteViewSet,
                   basename="favorites")
router_v1.register(r'purchases', PurchaseViewSet,
                   basename="purchase")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
