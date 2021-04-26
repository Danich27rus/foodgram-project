from django.db import models


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
            return super().get_queryset().filter(user=user).recipes.count()
        except self.model.DoesNotExist:
            return 0

    def list(self, user):
        try:
            return super().get_queryset().filter(user=user).all()
        except self.model.DoesNotExist:
            return []
