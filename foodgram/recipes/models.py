from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Ingredients(models.Model):

    name = models.CharField(_(""), max_length=200)
    qty = models.IntegerField(_(""))
    unit = models.ForeignKey(Units,
                             verbose_name=_(""),
                             on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name = class Ingredients")

    def __str__(self):
        return self.name


class Units(models.Model):

    name = models.CharField(_(""), max_length=20)

    class Meta:
        verbose_name = class Units")
        verbose_name_plural = class Unitss")

    def __str__(self):
        return self.name

