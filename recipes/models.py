import random
import string

from colorful.fields import RGBColorField
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def RandomString(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class Tag(models.Model):

    name = models.CharField(max_length=10)
    color = RGBColorField(colors=['#00ff00', '#ff0000', '#ffff00'])
    color_slug = models.SlugField(default='Black')
    slug = models.SlugField(default=RandomString(5))

    def __str__(self):
        return self.slug

    class Meta:
        unique_together = ('name', 'color', 'slug')
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Product(models.Model):

    title = models.CharField(max_length=100)
    dimension = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.dimension}'

    class Meta:
        ordering = ('title', )
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='author',
        related_name='recipe'
    )

    title = models.CharField(max_length=50)

    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)

    pic = models.ImageField(upload_to='meals/%Y-%m-%d')

    description = models.TextField()

    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    ingredients = models.ManyToManyField(
        Product,
        related_name='recipe',
        through='Ingredient',
        blank=True,
    )

    slug = models.SlugField()

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        ordering = ('-pub_date', 'title',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredient')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='ingredient')
    qty = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.recipe} - {self.qty}'

    class Meta:
        ordering = ('product', )
        verbose_name = 'Ингредиент'
        unique_together = ('recipe', 'product', )


class FavoriteManager(models.Manager):

    def get_tag_filtered(self, user, tags):
        try:
            recipes = super().get_queryset().get(user=user).recipes.all()
            if tags:
                return recipes.prefetch_related(
                    'author', 'tags'
                ).filter(
                    tags__slug__in=tags
                ).distinct()
            else:
                return recipes.prefetch_related(
                    'author', 'tags'
                ).all()
        except ObjectDoesNotExist:
            return []


class Favorite(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)
    manager = FavoriteManager()

    class Meta:
        ordering = ('user', )
        verbose_name = 'Избранное'


class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='followed',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Последователь: '{self.follower}', автор: '{self.author}'"

    class Meta:
        ordering = ('follower', )
        verbose_name = 'Подписки'


class PurchaseManager(models.Manager):

    def count(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.count()
        except ObjectDoesNotExist:
            return 0

    def list(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.all()
        except ObjectDoesNotExist:
            return []


class Purchase(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')
    recipes = models.ManyToManyField(Recipe)
    manager = PurchaseManager()

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
