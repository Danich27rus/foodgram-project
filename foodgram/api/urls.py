from .views import (GetIngredients, FollowTo, FollowDelete, FavoriteView,
                    PurchaseView)
from django.urls import path


urlpatterns = [
    path('subscriptions', FollowTo.as_view(), name='follow_to'),
    path('subscriptions/<int:author_id>', FollowDelete.as_view(),
         name='follow_delete'),

    path('favorites', FavoriteView.as_view(), name='favorite_view'),
    path('favorites/<int:recipe_id>', FavoriteView.as_view(),
         name='favorite_delete'),

    path('purchases', PurchaseView.as_view(), name='purchase'),
    path('purchases/<int:recipe_id>', PurchaseView.as_view(),
         name='purchase_delete'),

    path('ingredients/', GetIngredients.as_view(), name='ingredients'),
]
