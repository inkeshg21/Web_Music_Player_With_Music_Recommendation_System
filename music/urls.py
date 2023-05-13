from django.urls import path

from music import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('browse', views.browse, name='browse'),
    path('play-music/<str:type>/<int:id>', views.play_music, name='index'),
    path('add-to-playlist/<int:id>', views.add_to_playlist, name='add-to-playlist'),
    path('playlist', views.show_playlist, name='playlist'),
    path('delete-playlist/<int:id>', views.delete_playlist, name='delete-playlist'),
    path('browse-artists', views.browse_artists, name='browse-artists'),
    path('artist-songs/<int:artist_id>', views.artists_songs, name='artist-songs'),
    path('history', views.history, name='history'),
    path('delete-from-history/<int:id>',
         views.delete_from_history, name='delete-from-history'),
    path('delete-all-history', views.delete_all_history, name='delete-all-history'),
    path('music/<int:id>', views.music_details, name='music_details')
]
