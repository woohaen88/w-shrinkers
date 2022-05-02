from shortener.index.views import index, signup, signin, signout
from django.urls import path

app_name = "index"

urlpatterns = [
    path("", index, name="index"),
    path("register", signup, name="signup"),
    path("signin", signin, name="signin"),
    path("signout", signout, name="signout"),
]