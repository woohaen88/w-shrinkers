# import path 경로 => localhost:8000/urls/

from django.urls import path
from shortener.urls.views import url_list, url_create, url_change

app_name = "urls"
urlpatterns = [
    path("", url_list, name="url_list"),
    path("create/", url_create, name="url_create"),
    path("<str:action>/<int:url_id>/", url_change, name="url_change"),
]