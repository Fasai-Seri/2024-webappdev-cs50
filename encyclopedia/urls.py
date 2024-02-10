from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random", views.random_page, name="random_page"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("<str:entry>", views.show, name="show"),
]
