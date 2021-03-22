from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import RecipeForm
from .models import (Favorite, Follow, Ingredient, Product, Purchase, Recipe,
                     Tag)
from .utils import styles

User = get_user_model()


def get_form_ingredients(ingredients, recipe):

    result = list()
    for ingredient in ingredients:
        product = Product.objects.get(
            title=ingredient['title'],
            dimension=ingredient['unit']
        )
        result.append(
            Ingredient(
                recipe=recipe,
                product=product,
                qty=ingredient['qty'],
            )
        )
    return result


@login_required
@require_http_methods(['GET', 'POST'])
def new_view(request):

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        ingredients = form.cleaned_data['ingredients']
        form.cleaned_data['ingredients'] = []
        recipe.save()
        Ingredient.objects.bulk_create(
            get_form_ingredients(ingredients, recipe)
        )
        return redirect('index')
    tags = Tag.objects.all()
    context = {
        'page_title': 'Создание рецепта',
        'button': 'Создать рецепт',
        'tags': tags,
        'form': form,
        'style': styles.get('form')
    }
    return render(request, "recipes/formRecipe.html", context)


@require_http_methods(['GET'])
def recipe_view(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'page_title': recipe.title,
        'recipe': recipe,
        'style': styles.get('single')
    }
    return render(request, "recipes/singlePage.html", context)


@login_required
@require_http_methods(['GET'])
def delete_view(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('index')


@login_required
@require_http_methods(['GET', 'POST'])
def edit_view(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', recipe_id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )
        if form.is_valid():
            recipe.ingredients.remove()
            recipe.ingredient.all().delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            ingredients = form.cleaned_data['ingredients']
            form.cleaned_data['ingredients'] = []
            form.save()
            Ingredient.objects.bulk_create(
                get_form_ingredients(ingredients, recipe)
            )
            return redirect('recipe_view', recipe_id=recipe_id)
    form = RecipeForm(instance=recipe)
    tags = Tag.objects.all()
    checked_tags = recipe.tags.all()
    context = {
        'recipe_id': recipe_id,
        'page_title': 'Редактирование рецепта',
        'button': 'Сохранить',
        'tags': tags,
        'checked_tags': checked_tags,
        'form': form,
        'recipe': recipe,
        'edit': True,
        'style': styles.get('form')
    }
    return render(request, "recipes/formRecipe.html", context)


class IndexView(View):

    def get_queryset(self, request):

        tags = request.GET.getlist('filters')
        if not tags:
            recipes = Recipe.objects.exclude(
                tags__slug__in=tags)
        else:
            recipes = Recipe.objects.filter(
                tags__slug__in=tags)
        return recipes

    def get(self, request, tag_slug=None):

        recipes = self.get_queryset(request)
        paginator = Paginator(recipes, 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        tags = Tag.objects.all()
        context = {
            'page_title': 'Рецепты',
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'style': styles.get('index')
        }
        return render(
            request,
            "recipes/index.html",
            context
        )


@method_decorator(login_required, name='dispatch')
class Follows(View):

    def get(self, request):

        follows = Follow.objects.filter(
            follower=request.user).order_by('pk')
        page_num = request.GET.get('page')
        paginator = Paginator(follows, 6)
        page = paginator.get_page(page_num)
        context = {
            'page_title': 'Мои подписки',
            'active': 'subscription',
            'paginator': paginator,
            'page': page,
            'style': styles.get('follow'),
        }
        return render(request, "recipes/myFollow.html", context)


@method_decorator(login_required, name='dispatch')
class FavoritesView(View):

    def get_queryset(self, request, user):

        tags = request.GET.getlist('filters')
        try:
            if not tags:
                recipes = Favorite.manager.get(user=user).recipes.all()
            else:
                recipes = Favorite.manager.get(user=user).recipes.filter(
                    tags__slug__in=tags)
        except ObjectDoesNotExist:
            return []
        return recipes

    def get(self, request):

        user = request.user
        recipes = self.get_queryset(request, user)
        paginator = Paginator(recipes, 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        tags = Tag.objects.all()
        context = {
            'page_title': 'Избранное',
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'style': styles.get('index'),
        }
        return render(request, "recipes/index.html", context)


@method_decorator(login_required, name='dispatch')
class PurchaseView(View):

    def get(self, request):

        recipes = Purchase.manager.list(user=request.user)
        context = {
            'page_title': 'Список покупок',
            'recipes': recipes,
            'active': 'purchase',
            'style': styles.get('shoplist'),
        }
        return render(request, "recipes/shopList.html", context)


@method_decorator(login_required, name='dispatch')
class GetShopList(View):

    def get(self, request):

        user = request.user
        ingredients = (
            Ingredient.objects.select_related('product').
            filter(recipe__purchase__user=user).
            values('product__title', 'product__dimension').
            annotate(total=Sum('qty'))
        )
        filename = f'{user.username}_list.txt'
        products = []
        for ingredient in ingredients:
            products.append(
                f"{ingredient['product__title']}, "
                f"{ingredient['product__dimension']}, "
                f"{ingredient['total']}"
                "\n"
            )
        content = ''.join(products)
        response = HttpResponse(content, content_type='txt/plain')
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


def page_not_found(request, exception):
    return render(
        request, '404.html',
        {
            'path': request.path,
            'style': styles.get('index'),
            'title': 'Ошибка 404',
        },
        status=404
    )


def server_error(request):
    return render(
        request, '500.html',
        {
            'path': request.path,
            'style': styles.get('index'),
            'title': 'Ошибка 500',
        },
        status=500
    )


def permission_denied(request, exception):
    return render(
        request, '403.html',
        {
            'path': request.path,
            'style': styles.get("index"),
            'title': 'Ошибка 403',
        },
        status=403
    )
