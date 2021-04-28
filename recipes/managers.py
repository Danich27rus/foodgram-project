from django.db import models
import recipes.models as rmodels


class FavoriteManager(models.Manager):

    def get_tag_filtered(self, user, tags):
        try:
            recipes = super().get_queryset().get(user=user).recipes.all()
            if tags:
                return recipes.prefetch_related(
                    "author", "tags"
                ).filter(
                    tags__slug__in=tags
                ).distinct()
            else:
                return recipes.prefetch_related(
                    "author", "tags"
                ).all()
        except self.model.DoesNotExist:
            return []


class PurchaseManager(models.Manager):

    def count(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.count()
        except self.model.DoesNotExist:
            return 0

    def list(self, user):
        try:
            return rmodels.Recipe.objects.filter(purchases__user=user)
            # TODO not django/oop way?
            # return super().get_queryset().get(user=user).recipes.all()
        except self.model.DoesNotExist:
            return []
