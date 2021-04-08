from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage as storage
from django.urls import include, path
from django.views.generic.base import RedirectView

handler404 = "foodgram.views.page_not_found"  # noqa
handler500 = "foodgram.views.server_error"  # noqa
handler403 = "foodgram.views.permission_denied"  # noqa

urlpatterns = [
    path("", include("recipes.urls")),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("api/", include("api.urls")),
    path("favicon.ico", RedirectView.as_view(url=storage.url("favicon.ico"))),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
