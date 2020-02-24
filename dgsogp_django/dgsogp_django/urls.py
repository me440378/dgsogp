from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
	#'''favicon.ico'''
	# path('favicon.ico', serve, {'path': 'img/favicon.ico'}),
	###admin
    path(r'admin/', admin.site.urls),
    ###frontend-vue.js
    path(r'', TemplateView.as_view(template_name="index.html")),
    ###rest-framework
    path(r'api-auth/', include('rest_framework.urls')),
    # path(r'api-test/', include(router.urls)),
    ###backend
    path(r'api/1.0/', include('backend.urls')),
]
