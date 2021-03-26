from .models import Ingredient, Product


styles = {"index": "./pages/index.css",
          "form": "./pages/form.css",
          "shoplist": "./pages/shopList.css",
          "single": "./pages/single.css",
          "follow": "./pages/myFollow.css",
          }


def get_form_ingredients(ingredients, recipe):

    result = list()
    for ingredient in ingredients:
        product = Product.objects.get(
            title=ingredient['title'],
            dimension=ingredient['unit']
        )
        result.append(
            Ingredient(
                recipe=recipe,
                product=product,
                qty=ingredient['qty'],
            )
        )
    return result
