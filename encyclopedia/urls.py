from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.show, name="show"),
    path("wiki/<str:entry>/create", views.create, name="create"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("wiki/<str:entry>/save", views.save, name="save"),
    path("random", views.randomize, name="random")
]
