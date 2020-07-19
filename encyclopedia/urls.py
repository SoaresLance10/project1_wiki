from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("wiki/<title>", views.topic, name="topic"),
    path("edit/<title>", views.edit, name="edit"),
    path("rand", views.rand, name="rand")
]
