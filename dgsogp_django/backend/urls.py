from django.urls import include, path, re_path

from backend.views import index
from backend.views import UsersView
from backend.views import UsersDetailView
from backend.views import PasswordView
from backend.views import ForcePasswordView
from backend.views import LoginView

urlpatterns = [
	##index,在views/__init__.py
    path(r'', index, name='index'),
    ##UsersView
    path(r'users', UsersView.as_view()),
    re_path(r'users/(?P<id>\d+)', UsersDetailView.as_view()),
    re_path(r'users/password/(?P<id>\d+)', PasswordView.as_view()),
    re_path(r'users/forcepassword/(?P<id>\d+)', ForcePasswordView.as_view()),
    path(r'users/login', LoginView.as_view()),
    ##DatasourcesView
    ##MetadataView
]