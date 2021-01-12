from django.conf import settings
from django.db import models


class Unit(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Duration(models.Model):

    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Badge(models.Model):

    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Ingredient(models.Model):

    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} - {self.qty} {self.unit}'

    class Meta:
        ordering = ('name', )


class Recipe(models.Model):

    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='author'
    )
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    pic = models.ImageField(upload_to='meals/%Y-%m-%d')
    description = models.TextField()
    duration = models.IntegerField()
    duration_unit = models.ForeignKey(Duration, on_delete=models.SET_NULL,
                                      null=True)
    ingredients = models.ManyToManyField(Ingredient)
    slug = models.SlugField()
    badge = models.ManyToManyField(Badge)

    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        ordering = ('-pub_date', )


class Favorites(models.Model):

    follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower} - {self.recipe}'


class Follow(models.Model):
    # пользователь, который подписывается
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='follower',
        on_delete=models.CASCADE
    )
    # пользователь, на которого подписывются
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Последователь: '{self.follower}', автор: '{self.author}'"
