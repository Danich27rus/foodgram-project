from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteView, FollowView, GetIngredients, PurchaseView,
                    IngredientsViewSet, FollowDestroyViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'ingredients', IngredientsViewSet, basename="ingredienst")
router_v1.register(r'subscriptions', FollowDestroyViewSet,
                   basename="subscriptions")

urlpatterns = [
#     path("v1/subscriptions/", FollowView.as_view(), name="follow_to"),
#     path("v1/subscriptions/<int:author_id>/", FollowView.as_view(),
#          name="follow_delete"),

    path("v1/favorites/", FavoriteView.as_view(), name="favorite_view"),
    path("v1/favorites/<int:recipe_id>/", FavoriteView.as_view(),
         name="favorite_delete"),

    path("v1/purchases/", PurchaseView.as_view(), name="purchase"),
    path("v1/purchases/<int:recipe_id>/", PurchaseView.as_view(),
         name="purchase_delete"),

    path("v1/", include(router_v1.urls))
]
