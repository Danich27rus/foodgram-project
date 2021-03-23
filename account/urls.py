from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from account import views

urlpatterns = [path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'),
               path('signin/', views.signin, name='signin'),
               path('signup', views.signup, name='signup'),
               path('logout/', auth_views.LogoutView.as_view(),
                    {'next_page': reverse_lazy('index')}, name='logout'),
               path('change/', views.change_password, name='change'),
               path('activate/<slug:uidb64>/<slug:token>/', views.activate,
                    name='activate'),
               path('reset_confirm/<slug:uidb64>/<slug:token>/',
                    views.reset_confirm,
                    name="reset_password_confirm"),
               path('reset/', views.reset_password, name='reset'),
               ]
