"""troptimal URL Configuration

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
from troptimal_app import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.home, name='home'), #r indicates a regular expression. ^ indicates string matching. $ indicates the end. Thus, ^$ indicates matching an empty string - this is the home page URL for our app. It has nothing after the main url: http://127.0.0.1:8000/
    url(r'^trop_request/$', views.make_trop_request, name='trop_request'),
    url(r'^trop_request/attractions/(?P<trop_request_num>\w+)/$', views.selections, name='trop_name'),
    url(r'^trop_request/attractions/(?P<trop_request_num>\w+)/selections/$', views.schedule, name='selections'),
    url(r'^trop_request/attractions/(?P<trop_request_num>\w+)/selections/schedule/$', views.optimize_schedule, name='optimize')
]
