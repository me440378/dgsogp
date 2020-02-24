from django.urls import include, path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'users/', views.UsersView.as_view()),
    path(r'users/password', views.PasswordView.as_view()),
    path(r'users/forcepassword', views.ForcePasswordView.as_view())
]