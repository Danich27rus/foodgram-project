from django import forms
from django.contrib.auth import get_user_model

from .models import Product, Recipe, Tag, Ingredient
from .utils import get_form_ingredients

User = get_user_model()


class RecipeForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "tags__checkbox"}),
        to_field_name="slug",
        required=True,
    )

    description = forms.CharField(required=True)

    class Meta:

        model = Recipe

        fields = (
            "title", "description", "ingredients",
            "duration", "pic", "tags")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form__input"}),
            "description": forms.Textarea(
                attrs={"class": "form__textarea", "rows": "8"}),
            "duration": forms.NumberInput(
                attrs={"class": "form__input", "id": "id_time",
                       "name": "time"}),
        }

        labels = {
            "image": "Загрузить фото"
        }

    def clean_ingredients(self):

        ingredient_names = [
            self.data[key]
            for key in self.data
            if key.startswith("nameIngredient_")
        ]

        ingredient_units = [
            self.data[key]
            for key in self.data
            if key.startswith("unitsIngredient_")
        ]

        ingredient_quantities = [
            self.data[key]
            for key in self.data
            if key.startswith("valueIngredient_")
        ]

        ingredients_clean = []

        for ingredient in zip(ingredient_names, ingredient_units,
                              ingredient_quantities):
            if not int(ingredient[2]) > 0:
                raise forms.ValidationError("Количество ингредиентов должно "
                                            "быть больше нуля.")
            elif not Product.objects.filter(title=ingredient[0]).exists():
                raise forms.ValidationError(
                    "Ингредиенты должны быть из списка")
            else:
                ingredients_clean.append({"title": ingredient[0],
                                          "unit": ingredient[1],
                                          "quantity": ingredient[2]})

        if len(ingredients_clean) == 0:
            raise forms.ValidationError("Добавьте ингредиент")
        return ingredients_clean

    def save(self, author=None):
        recipe = super().save(commit=False)
        recipe.author = author
        ingredients = self.cleaned_data["ingredients"]
        self.cleaned_data["ingredients"] = []
        recipe = super().save()
        Ingredient.objects.bulk_create(
            get_form_ingredients(ingredients, recipe)
        )
        return recipe
