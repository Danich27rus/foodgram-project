from colorful.fields import RGBColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .managers import FavoriteManager
from .utils import random_string

User = get_user_model()

GREEN_COLOR = "#00ff00"
RED_COLOR = "#ff0000"
YELLOW_COLOR = "#ffff00"
BLACK_COLOR = "#000000"


class Tag(models.Model):

    name = models.CharField(max_length=10,
                            verbose_name="время приема")

    color = RGBColorField(colors=[GREEN_COLOR, RED_COLOR, YELLOW_COLOR],
                          max_length=10, verbose_name="цвет тэга")

    color_slug = models.SlugField(default=BLACK_COLOR,
                                  verbose_name="слаг цвета")

    slug = models.SlugField(default=random_string(5),
                            verbose_name="слаг тэга")

    class Meta:
        unique_together = ("name", "color", "color_slug", "slug")
        verbose_name = "тэг"
        verbose_name_plural = "тэги"

    def __str__(self):
        return self.name


class Product(models.Model):

    title = models.CharField(
        max_length=100,
        verbose_name="название"
    )

    dimension = models.CharField(
        max_length=50,
        verbose_name="единица"
    )

    class Meta:
        ordering = ("title", )
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

    def __str__(self):
        return f"{self.title} - {self.dimension}"

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super().save()


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="author",
        related_name="recipes",
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
        related_name="recipes",
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
        related_name="recipe_ingredients",
        verbose_name="рецепт"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="ingredient_product",
        verbose_name="продукт"
    )

    quantity = models.PositiveIntegerField(verbose_name="количество")

    def __str__(self):
        return f"{self.recipe.title} - {self.product.title} - {self.quantity}"

    class Meta:
        ordering = ("product", )
        verbose_name = "Ингредиент"
        unique_together = ("recipe", "product", )


class Favorite(models.Model):

    user = models.ForeignKey(User,
                             related_name="favorites",
                             on_delete=models.CASCADE,
                             verbose_name="пользователь")

    recipes = models.ForeignKey(Recipe,
                                verbose_name="рецепты",
                                on_delete=models.CASCADE,
                                related_name="favorites")

    manager = FavoriteManager()

    def __str__(self):
        return f"{self.user.username} - {self.recipes.title}"

    class Meta:
        ordering = ("user", )
        verbose_name = "избранное"
        verbose_name_plural = "избранные"


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

    class Meta:
        ordering = ("follower", )
        verbose_name = "подписки"

    def __str__(self):
        return (f"Автор {self.author.username}, "
                f"последователь {self.follower.username}")


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
        related_name="purchases",
        verbose_name="пользователь"
    )

    recipes = models.ManyToManyField(Recipe, verbose_name="рецепты")

    manager = PurchaseManager()

    class Meta:
        verbose_name = "покупка"
        verbose_name_plural = "покупки"

    def __str__(self):
        ls = ''.join(list(self.manager.list(self.user)))
        return f"Пользователь {self.user.username}, покупки {ls}"
