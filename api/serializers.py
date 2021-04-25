from django.contrib.auth import get_user_model

from recipes.models import Favorite, Follow, Purchase, Product
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Product


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Follow
        read_only_fields = ["follower", "author"]
