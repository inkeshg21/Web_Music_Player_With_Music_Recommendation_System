from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from account.auth import admin_only
from .forms import MusicForm
from django.shortcuts import render, redirect
from django.contrib import messages
from music.models import Music


# Create your views here.
def add_music(request):
    if request.method == 'POST':
        data = request.POST
        form = MusicForm(request.POST)
        title = data.get('title')
        singer = data.get('singer')
        genre = data.get('genre')
        description = data.get('description')

        file = request.FILES.get('file')
        poster = request.FILES.get('poster')
        cover = request.FILES.get('cover')

        music = Music.objects.create(uploader=request.user, title=title, singer=singer, genre=genre,
                                     description=description)
        if music:
            if file:
                music.file = file
            if poster:
                music.poster = poster
            if cover:
                music.cover = cover
            music.save()
            messages.success(request, "Music Uploaded.")
            return redirect('/admins/add-music')
        else:
            messages.error(request, "File upload failed!!")
    else:
        form = MusicForm()
    return render(request, 'admins/add-music.html', {'form': form})


def update_music(request, id):
    music = Music.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        title = data.get('title')
        singer = data.get('singer')
        genre = data.get('genre')
        description = data.get('description')
        music.title = title
        music.singer = singer
        music.genre = genre
        music.description = description

        file = request.FILES.get('file')
        poster = request.FILES.get('poster')
        cover = request.FILES.get('cover')

        if file:
            music.file = file
        if poster:
            music.poster = poster
        if cover:
            music.cover = cover

        if music:
            music.save()
            messages.success(request, "Music details updated")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "File update failed!")
    return render(request, 'admins/update-music.html', {'data': music})


def delete_music(request, id):
    music = Music.objects.get(id=id)
    music.delete()
    messages.success(request, "Song has been removed.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@admin_only
def music(request):
    musics = Music.objects.all().order_by('-date')
    context = {
        "musics": musics,
        'active_music': 'active'
    }
    return render(request, 'admins/music.html', context)
