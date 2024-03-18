from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("makingsoup", views.makesoup, name="makesoup"),
    path("htmx", views.htmx_test, name = "htmx"),
]
