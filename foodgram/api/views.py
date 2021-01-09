from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Recipe
# from my_project.example.models import Profile
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'recipes/index.html'

    def get(self, request):
        queryset = Recipe.objects.all()
        return Response({'recipes': queryset})
