from django.contrib import admin
from django.urls import include
from django.urls import path


urlpatterns = [
    path('', include('recipes.urls')),
    path('admin/', admin.site.urls),
    # path('api/', include('api.urls')),
    # path('redoc/', TemplateView.as_view(template_name='redoc.html'),
    #      name='redoc'),
]
