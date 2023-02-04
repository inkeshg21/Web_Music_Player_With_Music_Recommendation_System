from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from account.auth import user_only
from music.models import Music, Playlist
from django.contrib import messages


# Create your views here.
@user_only
def index(request):
    musics = Music.objects.all()
    context = {
        'musics': musics,
        'active_home': 'badge-primary text-primary rounded'
    }
    return render(request, 'music/index.html', context)


def play_music(request, id):
    music = Music.objects.get(id=id)
    context = {
        "music": music
    }

    html = render_to_string('player.html', context)

    return JsonResponse({"success": True, "data": html})


def add_to_playlist(request, id):
    music = Music.objects.get(id=id)
    playlist = Playlist.objects.create(music=music, user=request.user)
    playlistExist = Playlist.objects.get(music=music, user=request.user)
    if not playlistExist:
        playlist.save()
    else:
        messages.error(request, "Song already added to your playlist")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



def show_playlist(request):
    playlist = Playlist.objects.filter(user=request.user)
    context = {
        "playlist": playlist,
        "active_playlist": "badge-primary text-primary rounded"
    }
    return render(request, "music/playlist.html", context)


def delete_playlist(request, id):
    playlist = Playlist.objects.get(id=id)
    playlist.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
