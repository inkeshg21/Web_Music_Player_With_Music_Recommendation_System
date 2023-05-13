import datetime
import random
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from accounts.auth import user_only
from music.models import Artist, History, Music, Playlist, Rating
from django.contrib import messages

from music.utils import recommend_songs


# Create your views here.
@login_required
@user_only
def index(request):
    musics = Music.objects.all()
    recents = History.objects.filter(user=request.user).order_by('-date')
    recommendations = []
    for i in range(len(recents[:5])):
        recommend = recommend_songs(recents[i].music.title)
        for r in recommend:
            song = Music.objects.filter(title=r).first()
            recommendations.append(song)

    recommendations = list(set(recommendations))
    print(recommendations)
    context = {
        'musics': musics,
        'recents': recents,
        'active_home': 'badge-primary text-primary rounded',
        'recommendations': recommendations
    }
    return render(request, 'music/index.html', context)


@user_only
def about(request):
    return render(request, 'music/about.html', {'active_about': 'badge-primary text-primary rounded'})


@login_required
@user_only
def browse(request):
    musics = Music.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        musics = Music.objects.filter(title__icontains=search)
        context = {
            'musics': musics,
            'active_browse': 'badge-primary text-primary rounded'
        }
        return render(request, 'music/browse.html', context)

    else:
        context = {
            'musics': musics,
            'active_browse': 'badge-primary text-primary rounded'
        }
    return render(request, 'music/browse.html', context)


@login_required
@user_only
def play_music(request, type, id):

    music = random.choice(list(Music.objects.all()))
    songs = list(Music.objects.all())
    next_issue = random.choice(songs)
    prev_issue = random.choice(songs)

    if type == 'songs':
        music = Music.objects.get(id=id)
        print(music)
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
@user_only
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
@user_only
def show_playlist(request):
    playlist = Playlist.objects.filter(user=request.user).order_by('id')
    context = {
        "playlist": playlist,
        "active_playlist": "badge-primary text-primary rounded"
    }
    return render(request, "music/playlist.html", context)


@login_required
@user_only
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
    messages.success(request, "Song removed from history")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_all_history(request):
    history = History.objects.filter(user=request.user)
    history.delete()
    messages.success(request, "Song history has been cleared")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def music_details(request, id):
    music = Music.objects.get(id=id)
    ratings = Rating.objects.filter(song=id)
    recommendations = []
    try:
        recommendation = recommend_songs(music.title)
        for r in recommendation:
            song = Music.objects.filter(title=r).first()
            recommendations.append(song)
        # next = random.choice(recommendation).id

        recommendations = list(set(recommendations))
    except Exception as e:
        print(e)

    if len(recommendations) == 0:
        recommendations = Music.objects.all()[:10]

    if request.method == 'POST':
        data = request.POST
        rate = data.get('rating')
        comment = data.get('comment')

        ratingExist = Rating.objects.filter(
            user=request.user.id, song=id).first()

        if not ratingExist:
            rating = Rating.objects.create(
                user=request.user, song=music, rating=rate, comment=comment)
            rating.save()
            messages.success(request, "Song review submitted successfully.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "You have already rated this song.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    context = {
        'music': music,
        'recommendation': recommendations,
        'ratings': ratings,
        'next': next
    }
    return render(request, 'music/music_details.html', context)


@user_only
def browse_artists(request):
    artists = Artist.objects.all()
    for artist in artists:
        artist.songs = Music.objects.filter(artist=artist.id).count()
    context = {
        'active_artists': "badge-primary text-primary rounded",
        'artists': artists
    }

    return render(request, 'music/artists.html', context)


@user_only
def artists_songs(request, artist_id):
    artist = Artist.objects.filter(id=artist_id).first()
    if not artist:
        messages.error(request, "Failed to get artists data.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    music = Music.objects.filter(artist=artist.id).order_by('-date')
    context = {
        "songs": music,
        'artist': artist
    }
    return render(request, "music/artists-songs.html", context)
