import json
from urllib.parse import unquote

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

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


@method_decorator(login_required, name="dispatch")
class FollowTo(View):

    def post(self, request):

        json_data = json.loads(request.body.decode())
        author = get_object_or_404(User, id=json_data["id"])
        data = {"success": True}
        obj, created = Follow.objects.get_or_create(follower=request.user,
                                                    author=author)
        if not created:
            data["success"] = False
        return JsonResponse(data)


@method_decorator(login_required, name="dispatch")
class FollowDelete(View):

    def delete(self, request, author_id):

        author = get_object_or_404(User, id=author_id)
        follow = author.followed.filter(follower=request.user)
        quantity, obj_subscription = follow.delete()
        if quantity == 0:
            data = {"success": False}
        else:
            data = {"success": True}
        return JsonResponse(data)


@method_decorator(login_required, name="dispatch")
class FavoriteView(View):

    def post(self, request):

        json_data = json.loads(request.body.decode())
        recipe_id = json_data["id"]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {"success": True}
        favorite, created = Favorite.manager.get_or_create(user=request.user)
        is_favorite = Favorite.manager.filter(id=recipe_id).exists()
        if is_favorite:
            data["success"] = False
        else:
            favorite.recipes.add(recipe)
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
