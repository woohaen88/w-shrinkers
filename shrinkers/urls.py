"""shrinkers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shortener.views import index, signup, signin, signout, url_list, url_create, url_change

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index" ),
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("urls", url_list, name="url_list"),
    path("urls/create", url_create, name="url_create"),
    path("urls/<str:action>/<int:url_id>", url_change, name="url_change"),
]
