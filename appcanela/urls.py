from django.contrib import admin
from django.urls import path
from django.urls import include, path
from .views import index

urlpatterns = [
    path(" ", index,name="index")
]
 