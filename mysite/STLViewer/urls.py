from django.urls import path

from . import views

urlpatterns = [
    path("item/", views.detailView, name="Detail-View"),
    path("index/", views.basicView, name="Basic-View" ),
]