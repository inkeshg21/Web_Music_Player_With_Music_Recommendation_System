from django.urls import path

from admins import views

urlpatterns = [
    path('', views.music),
    path('add-music', views.add_music),
    path('update-music/<int:id>', views.update_music),
    path('delete-music/<int:id>', views.delete_music),
]
