"""storytime URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from storytime.stories import views
import settings

urlpatterns = [
	url(r'^accounts/login$',views.custom_login),
	url(r'^accounts/', include('registration.backends.default.urls')),
	url(r'^stories/create_stories/',views.create_stories),
	url(r'^stories/read',views.read_stories),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
	url(r'^profile',views.user_profile),
	url(r'^relationship/unfollow',views.unfollow),
	url(r'^relationship/follow',views.follow),
	url(r'^',views.following),
]
