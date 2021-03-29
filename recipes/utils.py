import random
import string

import recipes.models as models


def get_form_ingredients(ingredients, recipe):

    result = list()
    for ingredient in ingredients:
        product = models.Product.objects.get(
            title=ingredient["title"],
            dimension=ingredient["unit"]
        )
        result.append(
            models.Ingredient(
                recipe=recipe,
                product=product,
                quantity=ingredient["quantity"],
            )
        )
    return result


def random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))
