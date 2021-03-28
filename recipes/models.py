from colorful.fields import RGBColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .utils import random_string

User = get_user_model()


class Tag(models.Model):

    name = models.CharField(max_length=10,
                            verbose_name="имя")
    color = RGBColorField(colors=["#00ff00", "#ff0000", "#ffff00"],
                          max_length=10, verbose_name="цвет тэга")
    color_slug = models.SlugField(default="Black",
                                  verbose_name="слаг цвета")
    slug = models.SlugField(default=random_string(5),
                            verbose_name="слаг тэга")

    def __str__(self):
        return self.slug

    class Meta:
        unique_together = ("name", "color", "color_slug", "slug")
        verbose_name = "тэг"
        verbose_name_plural = "тэги"


class Product(models.Model):

    title = models.CharField(
        max_length=100,
        verbose_name="название"
    )

    dimension = models.CharField(
        max_length=50,
        verbose_name="единица"
    )

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.dimension}"

    class Meta:
        ordering = ("title", )
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="author",
        related_name="recipe",
        verbose_name="автор",
    )

    title = models.CharField(
        max_length=50,
        verbose_name="название",
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="дата публикации"
    )

    pic = models.ImageField(upload_to="meals/%Y-%m-%d")

    description = models.TextField(verbose_name="описание")

    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="длительность"
    )

    ingredients = models.ManyToManyField(
        Product,
        related_name="recipe",
        through="Ingredient",
        blank=True,
        verbose_name="ингредиенты"
    )

    slug = models.SlugField(verbose_name="слаг")

    tags = models.ManyToManyField(Tag, verbose_name="тэги")

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        ordering = ("-pub_date", "title",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Ingredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient",
        verbose_name="рецепт"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="ingredient",
        verbose_name="продукт"
    )

    quantity = models.PositiveIntegerField(verbose_name="количество")

    def __str__(self):
        return f"{self.recipe} - {self.product} - {self.quantity}"

    class Meta:
        ordering = ("product", )
        verbose_name = "Ингредиент"
        unique_together = ("recipe", "product", )


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


class Favorite(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)
    manager = FavoriteManager()

    class Meta:
        ordering = ("user", )
        verbose_name = "Избранное"


class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE,
        verbose_name="последователь"
    )
    author = models.ForeignKey(
        User,
        related_name="followed",
        on_delete=models.CASCADE,
        verbose_name="автор"
    )

    def __str__(self):
        return f"Последователь: {self.follower}, автор: {self.author}"

    class Meta:
        ordering = ("follower", )
        verbose_name = "Подписки"


class PurchaseManager(models.Manager):

    def count(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.count()
        except self.model.DoesNotExist:
            return 0

    def list(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.all()
        except self.model.DoesNotExist:
            return []


class Purchase(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases"
    )

    recipes = models.ManyToManyField(Recipe)

    manager = PurchaseManager()

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
