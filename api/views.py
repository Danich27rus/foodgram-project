import json
from urllib.parse import unquote

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import ProductSerializer, FollowSerializer
from recipes.models import Favorite, Follow, Product, Purchase, Recipe

User = get_user_model()


@method_decorator(login_required, name="dispatch")
class GetIngredients(View):

    def get(self, request):

        query = unquote(request.GET.get("query"))
        data = list(
            Product.objects.filter(title__startswith=query).values("title",
                                                                   "dimension")
        )
        return JsonResponse(data, safe=False)


class IngredientsViewSet(ListModelMixin, GenericViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query")
        queryset = Product.objects.filter(title__startswith=query
                                          ).values("title", "dimension")
        return queryset


@method_decorator(login_required, name="dispatch")
class FollowView(View):

    def post(self, request):

        json_data = json.loads(request.body.decode())
        author = get_object_or_404(User, id=json_data["id"])
        data = {"success": True}
        obj, created = Follow.objects.get_or_create(follower=request.user,
                                                    author=author)
        if not created:
            data["success"] = False
        return JsonResponse(data)

    def delete(self, request, author_id):

        author = get_object_or_404(User, id=author_id)
        follow = author.followed.filter(follower=request.user)
        quantity, obj_subscription = follow.delete()
        if quantity == 0:
            data = {"success": False}
        else:
            data = {"success": True}
        return JsonResponse(data)


class FollowDestroyViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = 'author'

    def perform_create(self, serializer):
        
        author = User.objects.get(id=self.request.data["id"])
        follower = self.request.user
        serializer.save(author=author, follower=follower)
        return super().perform_create(serializer)

    def destroy(self, request, *args, **kwargs):

        author_id = kwargs.get("author")
        user = request.user
        author = get_object_or_404(User, id=author_id)
        follow = author.followed.filter(follower=user)
        data = self.perform_destroy(follow)
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):

        quantity, obj = instance.delete()
        if quantity == 0:
            data = {"success": False}
        else:
            data = {"success": True}
        return data


@method_decorator(login_required, name="dispatch")
class FavoriteView(View):

    def post(self, request):

        json_data = json.loads(request.body.decode())
        recipe_id = json_data["id"]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {"success": True}
        favorite, created = Favorite.manager.get_or_create(user=request.user,
                                                           recipes=recipe)
        if not created:
            data["success"] = False
        return JsonResponse(data)

    def delete(self, request, recipe_id):

        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = Favorite.manager.filter(user=request.user, recipes=recipe)
        count, favorites = favorite.delete()
        if count == 0:
            data = {"success": False}
        else:
            data = {"success": True}
        return JsonResponse(data)


@method_decorator(login_required, name="dispatch")
class PurchaseView(View):

    def post(self, request):

        json_data = json.loads(request.body.decode())
        recipe_id = json_data["id"]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase, created = Purchase.manager.get_or_create(user=request.user)
        data = {"success": True}
        if not Purchase.manager.filter(recipes=recipe,
                                       user=request.user).exists():
            purchase.recipes.add(recipe)
            return JsonResponse(data)
        data["success"] = False
        return JsonResponse(data)

    def delete(self, request, recipe_id):

        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {"success": True}
        try:
            purchase = Purchase.manager.get(user=request.user)
        except Purchase.DoesNotExist:
            data["success"] = False
        if not purchase.recipes.filter(id=recipe_id).exists():
            data["success"] = False
        purchase.recipes.remove(recipe)
        return JsonResponse(data)
