from django.urls import path

from music import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play-music/<int:id>', views.play_music, name='index'),
    path('add-to-playlist/<int:id>', views.add_to_playlist, name='add-to-playlist'),
    path('playlist', views.show_playlist, name='playlist'),
    path('delete-playlist/<int:id>', views.delete_playlist, name='delete-playlist'),
]
