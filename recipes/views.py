from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import RecipeForm
from .models import Follow, Ingredient, Purchase, Recipe, Tag

PER_PAGE = getattr(settings, "PAGINATOR_PER_PAGE", None)

User = get_user_model()


@login_required
@require_http_methods(["GET", "POST"])
def new_view(request):

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        recipe = form.save(author=request.user)
        return redirect("recipe_view", recipe_id=recipe.id)
    tags = Tag.objects.all()
    context = {
        "page_title": "Создание рецепта",
        "button": "Создать рецепт",
        "tags": tags,
        "form": form,
    }
    return render(request, "recipes/formRecipe.html", context)


@require_http_methods(["GET"])
def recipe_view(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        "page_title": recipe.title,
        "recipe": recipe,
    }
    return render(request, "recipes/singlePage.html", context)


@login_required
@require_http_methods(["GET"])
def delete_view(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect("index")


@login_required
@require_http_methods(["GET", "POST"])
def edit_view(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect("recipe_view", recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        recipe.recipe_ingredients.all().delete()
        form.save(author=request.user)
        return redirect("recipe_view", recipe_id=recipe_id)
    form = RecipeForm(instance=recipe)
    tags = Tag.objects.all()
    context = {
        "page_title": "Редактирование рецепта",
        "button": "Сохранить",
        "tags": tags,
        "form": form,
        "recipe": recipe,
        "edit": True,
    }
    return render(request, "recipes/formRecipe.html", context)


class IndexView(View):

    def get_queryset(self, request):

        tags = request.GET.getlist("filters")
        if not tags:
            recipes = Recipe.objects.exclude(
                tags__slug__in=tags)
        else:
            recipes = Recipe.objects.filter(
                tags__slug__in=tags).distinct()
        return recipes

    def get(self, request, tag_slug=None):

        recipes = self.get_queryset(request)
        paginator = Paginator(recipes, PER_PAGE)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)
        tags = Tag.objects.all()
        context = {
            "page_title": "Рецепты",
            "page": page,
            "paginator": paginator,
            "tags": tags,
        }
        return render(
            request,
            "recipes/index.html",
            context
        )


@method_decorator(login_required, name="dispatch")
class FollowsView(View):

    def get(self, request):

        follows = Follow.objects.filter(
            user=request.user).order_by("pk")
        page_num = request.GET.get("page")
        paginator = Paginator(follows, PER_PAGE)
        page = paginator.get_page(page_num)
        context = {
            "page_title": "Мои подписки",
            "active": "subscription",
            "paginator": paginator,
            "page": page,
        }
        return render(request, "recipes/myFollow.html", context)


@method_decorator(login_required, name="dispatch")
class FavoritesView(View):

    def get_queryset(self, request, user):

        tags = request.GET.getlist("filters")
        try:
            if not tags:
                recipes = Recipe.objects.filter(
                    favorite_recipes__user=user).distinct()
            else:
                recipes = Recipe.objects.filter(
                    favorite_recipes__user=user).filter(
                    tags__slug__in=tags)
        except Recipe.DoesNotExist:
            return []
        return recipes

    def get(self, request):

        user = request.user
        recipes = self.get_queryset(request, user)
        # recipes = Recipe.objects.all()
        paginator = Paginator(recipes, PER_PAGE)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)
        tags = Tag.objects.all()
        context = {
            "page_title": "Избранное",
            "page": page,
            "paginator": paginator,
            "tags": tags,
        }
        return render(request, "recipes/index.html", context)


@method_decorator(login_required, name="dispatch")
class PurchaseView(View):

    def get(self, request):

        recipes = Purchase.objects.list(user=request.user)
        context = {
            "page_title": "Список покупок",
            "recipes": recipes,
            "active": "purchase",
        }
        return render(request, "recipes/shopList.html", context)


@method_decorator(login_required, name="dispatch")
class GetShopList(View):

    def get(self, request):

        user = request.user
        ingredients = (
            Ingredient.objects.select_related("product").
            filter(recipe__purchases__user=user).
            values("product__title", "product__dimension").
            annotate(total=Sum("quantity"))
        )
        filename = f"{user.username}_list.txt"
        products = []
        for ingredient in ingredients:
            products.append(
                f"{ingredient['product__title']}, "
                f"{ingredient['product__dimension']}, "
                f"{ingredient['total']}"
                "\n"
            )
        content = ''.join(products)
        response = HttpResponse(content, content_type="txt/plain")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
