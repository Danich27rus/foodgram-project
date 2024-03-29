from django import template
from django.utils.safestring import mark_safe

from recipes.models import Favorite, Purchase

register = template.Library()


@register.filter
def subscribed(author, user):
    return author.followed.filter(user=user).exists()


@register.filter
def favorite(recipe, user):
    return Favorite.objects.filter(user=user, recipes=recipe).exists()


@register.filter(name='get_filter_values')
def get_values(value):
    return value.getlist('filters')


@register.filter
def badge_color(text, color):
    safe_text = ('<span style="color:{color}">{text}</span>'
                 .format(color=color, text=text))
    return mark_safe(safe_text)


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):

    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)

    return new_request.urlencode()


@register.filter
def purchased(recipe, user):

    return Purchase.objects.filter(recipes=recipe, user=user).exists()


@register.filter
def purchase_count(user):

    try:
        return Purchase.objects.filter(user=user).count()
    except Purchase.DoesNotExist:
        return 0
