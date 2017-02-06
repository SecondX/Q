"""myQQsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from restaurants.views import menu, list_restaurants,comment,set_c,get_c,index
from restaurants.views import IndexView, RestaurantView, MenuView
# from restaurants.views import login,logout
from django.contrib.auth.views import login, logout
from restaurants.views import session_test
from django.contrib import admin

urlpatterns = [
    # url(r'^menu/$', menu),
    url(r'^menu/(?P<id>\d+)$', MenuView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^restaurants_list/', list_restaurants),
    url(r'^restaurants_list/', RestaurantView.as_view()),
    url(r'^comment/(\d{1,5})/$', comment),
    url(r'setcookie/', set_c),
    url(r'getcookie/', get_c),
    url(r'sessiontest/', session_test),
    url(r'login/', login),
    url(r'logout/', logout),
    # url(r'index/', index),
    url(r'index/', IndexView.as_view()),
]
