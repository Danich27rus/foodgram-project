from django import template
from django.utils.safestring import mark_safe
from recipes.models import Favorite, Follow, Purchase

register = template.Library()


@register.filter
def subscribed(author, follower):
    return Follow.objects.filter(follower=follower).exists()


@register.filter
def favorite(recipe, user):
    return Favorite.manager.filter(user=user, recipes=recipe).exists()


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

    return Purchase.manager.filter(recipes=recipe, user=user).exists()


@register.filter
def purchase_count(user):

    try:
        return Purchase.manager.get(user=user).recipes.count()
    except Purchase.DoesNotExist:
        return 0
