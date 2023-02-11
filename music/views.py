import datetime
import random
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from accounts.auth import user_only
from music.models import History, Music, Playlist
from django.contrib import messages


# Create your views here.
@login_required
def index(request):
    musics = Music.objects.all()
    recents = History.objects.filter(user=request.user).order_by('-date')
    context = {
        'musics': musics,
        'recents': recents,
        'active_home': 'badge-primary text-primary rounded'
    }
    return render(request, 'music/index.html', context)


@login_required
def play_music(request, type, id):

    music = random.choice(list(Music.objects.all()))
    songs = list(Music.objects.all())
    next_issue = random.choice(songs)
    prev_issue = random.choice(songs)

    if type == 'songs':
        music = Music.objects.get(id=id)
    if type == 'playlist':
        songs = list(Playlist.objects.filter(user=request.user).order_by('id'))
        playlist = Playlist.objects.get(id=id)
        music = Music.objects.get(id=playlist.music.id)
        try:
            next_issue = songs[songs.index(playlist) + 1]
            prev_issue = songs[songs.index(playlist)-1]
        except:
            next_issue = songs[0]
            prev_issue = songs[-1]

    prev_his = History.objects.filter(music=music, user=request.user).first()
    if prev_his:
        prev_his.date = datetime.datetime.now()
        prev_his.save()
    else:
        history = History.objects.create(music=music, user=request.user)
        history.save()

    context = {
        "music": music,
        'next': next_issue.id,
        'prev': prev_issue.id,
        'type': type
    }

    html = render_to_string('player.html', context)

    return JsonResponse({"success": True, "data": html})


@login_required
def add_to_playlist(request, id):
    music = Music.objects.get(id=id)
    playlistExist = list(Playlist.objects.filter(
        music=music, user=request.user))
    print(len(playlistExist))
    if len(playlistExist) > 0:
        messages.error(request, "Song already added to your playlist")
    else:
        playlist = Playlist.objects.create(music=music, user=request.user)
        playlist.save()
        messages.success(request, "Song added to your playlist")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def show_playlist(request):
    playlist = Playlist.objects.filter(user=request.user).order_by('id')
    context = {
        "playlist": playlist,
        "active_playlist": "badge-primary text-primary rounded"
    }
    return render(request, "music/playlist.html", context)


@login_required
def delete_playlist(request, id):
    playlist = Playlist.objects.get(id=id)
    playlist.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def history(request):
    history = History.objects.filter(user=request.user).order_by('-date')
    return render(request, 'music/history.html', {'history': history})

@login_required
def delete_from_history(request, id):
    history = History.objects.get(id=id)
    history.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def delete_all_history(request):
    history = History.objects.filter(user=request.user)
    history.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
