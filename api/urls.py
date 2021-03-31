from django.urls import path

from .views import (FavoriteView, FollowDelete, FollowTo, GetIngredients,
                    PurchaseView)

urlpatterns = [
    path("v1/subscriptions", FollowTo.as_view(), name="follow_to"),
    path("v1/subscriptions/<int:author_id>/", FollowDelete.as_view(),
         name="follow_delete"),

    path("v1/favorites", FavoriteView.as_view(), name="favorite_view"),
    path("v1/favorites/<int:recipe_id>/", FavoriteView.as_view(),
         name="favorite_delete"),

    path("v1/purchases", PurchaseView.as_view(), name="purchase"),
    path("v1/purchases/<int:recipe_id>/", PurchaseView.as_view(),
         name="purchase_delete"),

    path("v1/ingredients/", GetIngredients.as_view(), name="ingredients"),
]
