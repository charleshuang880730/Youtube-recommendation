"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from search.views import hello_world
from search.views import MyOwnView
from search.views import MyOwnView2
from search.views import MyOwnView3
from search.views import MyOwnView4
from django.views.generic.base import TemplateView

from django.urls import include, path
from rest_framework import routers
from search import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'charles', views.CharlesViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^hello/$', hello_world),
	url(r'path/', TemplateView.as_view(template_name = "main_page.html")),
	url(r'test/', views.MyOwnView.as_view()),
	url(r'sendall/', views.MyOwnView2.as_view()),
	url(r'sendpop/', views.MyOwnView3.as_view()),
	url(r'sendkey/', views.MyOwnView4.as_view()),
	#url(r'^api/', include(router.urls))
	path('', include(router.urls)),
	#path('', router.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
