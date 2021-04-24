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

    id = serializers.IntegerField()

    def validate(self, attrs):
        self.follower = None
        self.author = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            self.follower = request.user
        self.author = User.objects.get(id=attrs.get("id"))
        return super().validate(attrs)

    class Meta:
        fields = "__all__"
        model = Follow
        read_only_fields = ["follower", "author"]
