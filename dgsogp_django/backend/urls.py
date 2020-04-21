from django.urls import include, path, re_path

from backend.views import index
from backend.views import UsersView
from backend.views import UsersDetailView
from backend.views import MessagesView
from backend.views import MessagesDetailView
from backend.views import PasswordView
from backend.views import ForcePasswordView
from backend.views import LoginView
from backend.views import DatasourcesView
from backend.views import DatasourcesDetailView
from backend.views import HadoopsourcesView
from backend.views import HadoopsourcesDetailView
from backend.views import MetadataView
from backend.views import MetadataDetailView
from backend.views import DatainterfacesView
from backend.views import DatainterfacesDetailView
from backend.views import DatainterfacesDataView
from backend.views import DatabaseinterfacesView
from backend.views import DatabaseinterfacesDetailView
#前端视图
from backend.views import FrontendView
from backend.views import HeaderView
from backend.views import DashboardView
from backend.views import DatasourceStateView
#WebSocket视图
from backend.views import DatabaseCommandLine

urlpatterns = [
	##index,在views/__init__.py
    path(r'', index, name='index'),
    ##UsersView
    path(r'users', UsersView.as_view()),
    re_path(r'users/(?P<id>\d+)', UsersDetailView.as_view()),
    re_path(r'users/password/(?P<id>\d+)', PasswordView.as_view()),
    re_path(r'users/forcepassword/(?P<id>\d+)', ForcePasswordView.as_view()),
    path(r'users/login', LoginView.as_view()),
    ##MessagesView
    path(r'messages', MessagesView.as_view()),
    re_path(r'messages/(?P<id>\d+)', MessagesDetailView.as_view()),
    ##DatasourcesView
    path(r'datasources', DatasourcesView.as_view()),
    re_path(r'datasources/(?P<id>\d+)', DatasourcesDetailView.as_view()),
    ##HadoopsourcesView
    path(r'hadoopsources', HadoopsourcesView.as_view()),
    re_path(r'hadoopsources/(?P<id>\d+)', HadoopsourcesDetailView.as_view()),
    ##MetadataView
    path(r'metadata', MetadataView.as_view()),
    re_path(r'metadata/(?P<id>\d+)', MetadataDetailView.as_view()),
    ##DatainterfacesView
    path(r'datainterfaces', DatainterfacesView.as_view()),
    re_path(r'datainterfaces/(?P<id>\d+)', DatainterfacesDetailView.as_view()),
    re_path(r'datainterfaces/data/(?P<id>\d+)', DatainterfacesDataView.as_view()),
    ##DatabaseinterfacesView
    path(r'databaseinterfaces', DatabaseinterfacesView.as_view()),
    re_path(r'databaseinterfaces/(?P<id>\d+)', DatabaseinterfacesDetailView.as_view()),
    ##Frontend 前端视图
    path(r'frontend/header', HeaderView.as_view()),
    path(r'frontend/dashboard', DashboardView.as_view()),
    re_path(r'frontend/dstate/(?P<id>\d+)', DatasourceStateView.as_view()),
    ##WebSocket 视图
    path(r'databaseinterfaces/dbcli', DatabaseCommandLine.dbcli)
]