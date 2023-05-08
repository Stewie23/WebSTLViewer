from django.urls import path



from . import views

urlpatterns = [
    path("item/", views.detailView, name="Detail-View"),
    path("index/", views.basicView, name="Basic-View" ),
    path("thumbeditor/", views.editThumbView, name="Thumb-View"),
    path("download/",views.download, name ="Download"),
    path("add/",views.create_item,name = "Add Item"),
    path("updateThumb",views.updateThumb,name="Update Thumb"),
]