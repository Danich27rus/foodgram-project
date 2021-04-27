from django.contrib.auth import get_user_model

from recipes.models import Favorite, Follow, Purchase, Product
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Product


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Follow
        read_only_fields = ["user", "author"]


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Favorite
        read_only_fields = ["user", "recipes"]


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Purchase
        read_only_fields = ["user", "recipes"]
