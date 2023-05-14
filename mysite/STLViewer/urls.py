from django.urls import path



from . import views

urlpatterns = [
    path("item/", views.detailView, name="Detail-View"),
    path("index/", views.basicView, name="Basic-View" ),
    path("thumbeditor/", views.editThumbView, name="Thumb-View"),
    path("new/", views.recentAdditions, name="Additions-View"),
    path("download/",views.download, name ="Download"),
    path("add/",views.create_item,name = "Add Item"),
    path("updateThumb",views.updateThumb,name="Update Thumb"),
    path('add_to_collection/<int:item_id>/', views.add_to_collection, name='add_to_collection'),
    path('collection/create_edit/', views.create_or_edit_collection, name='create_or_edit_collection'),
    path('collection/<int:pk>/', views.collection_detail, name='collection_detail'),
    path('collection/remove/<int:collection_id>/<int:item_id>/', views.remove_from_collection, name='remove_from_collection'),




]