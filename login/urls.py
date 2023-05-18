from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'login'
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("logout1/", views.logout_view, name="logout"),
]
