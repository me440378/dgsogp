from django.urls import include, path, re_path

from backend.views import index
from backend.views import UsersView
from backend.views import UsersDetailView
from backend.views import PasswordView
from backend.views import ForcePasswordView
from backend.views import LoginView
from backend.views import DatasourcesView
from backend.views import DatasourcesDetailView
from backend.views import MetadataView
from backend.views import MetadataDetailView

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
    path(r'datasources', DatasourcesView.as_view()),
    re_path(r'datasources/(?P<id>\d+)', DatasourcesDetailView.as_view()),
    ##MetadataView
    path(r'metadata', MetadataView.as_view()),
    re_path(r'metadata/(?P<id>\d+)', MetadataDetailView.as_view()),
]