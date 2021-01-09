from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from taggit.models import Tag
from .models import Recipe
from django.shortcuts import get_object_or_404, render

User = get_user_model()


def index(request, tag_slug=None):
    recipes_list = Recipe.objects.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        recipes_list = recipes_list.filter(tags__in=[tag])
    paginator = Paginator(recipes_list, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/index.html',
        {'page': page, 'paginator': paginator}
    )
