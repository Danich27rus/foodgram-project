from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('recipes/<int:recipe_id>/', views.recipe_view,
         name='recipe_view'),
    path('new/', views.new_view,
         name='recipe_new'),
    path('recipes/<int:recipe_id>/edit/', views.edit_view,
         name='recipe_edit'),
    path('recipes/<int:recipe_id>/delete/', views.delete_view,
         name='recipe_delete'),

    path('favorites/', views.FavoritesView.as_view(), name='favorites'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases_view'),

    path('follows/', views.Follows.as_view(), name='follows'),

    path('shoplist/', views.GetShopList.as_view(), name='shoplist'),
]
