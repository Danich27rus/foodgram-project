from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import (FavoriteSerializer, FollowSerializer,
                             ProductSerializer, PurchaseSerializer)
from recipes.models import Favorite, Follow, Product, Purchase, Recipe

User = get_user_model()


class ModCreateModelMixin(CreateModelMixin):

    # TODO: make more common to fit FollowViewSet
    def perform_create(self, serializer):

        recipe = Recipe.objects.get(id=self.request.data["id"])
        user = self.request.user
        serializer.save(user=user, recipes=recipe)
        return super().perform_create(serializer)


class ModDestroyModelMixin(DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            "user": request.user
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        # obj = queryset.filter(**filter_kwargs)
        data = self.perform_destroy(obj)
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):

        quantity, obj = instance.delete()
        if quantity == 0:
            data = {"success": False}
        else:
            data = {"success": True}
        return data


class IngredientsViewSet(ListModelMixin, GenericViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query")
        queryset = Product.objects.filter(title__startswith=query
                                          ).values("title", "dimension")
        return queryset


class FollowViewSet(CreateModelMixin, ModDestroyModelMixin, GenericViewSet):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = 'author'

    def perform_create(self, serializer):

        author = User.objects.get(id=self.request.data["id"])
        user = self.request.user
        serializer.save(author=author, user=user)
        return super().perform_create(serializer)


class FavoriteViewSet(ModCreateModelMixin, ModDestroyModelMixin, GenericViewSet):

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'recipes'


class PurchaseViewSet(ModCreateModelMixin, ModDestroyModelMixin, GenericViewSet):

    queryset = Purchase.objects.all().distinct()
    serializer_class = PurchaseSerializer
    lookup_field = 'recipes'
