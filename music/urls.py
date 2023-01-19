from django.urls import path

from music import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play-music/<int:id>', views.play_music, name='index'),
]