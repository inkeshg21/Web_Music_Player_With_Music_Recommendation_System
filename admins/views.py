from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from account.auth import admin_only
from .forms import MusicForm, UserUpdate
from django.shortcuts import render, redirect
from django.contrib import messages
from music.models import Music
from account.forms import RegistrationForm
from account.models import Profile

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


def users(request):
    users = User.objects.all().exclude(username=request.user)
    context = {
        "users": users,
        'active_users': 'active'
    }
    return render(request, 'admins/users.html', context)

# add new user


def add_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password2')
            user = User.objects.create(username=username, email=email)
            pofile = Profile.objects.create(user=user)
            user.set_password(password1)
            user.save()
            pofile.save()
            return redirect('/admins/add-user')
    else:
        form = RegistrationForm()
    return render(request, 'admins/add-user.html', {'form': form})

# update user


def update_user(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserUpdate(request.POST)
        form.fields['email'].initial = "email"
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            usernameExists = User.objects.filter(
                username=username).exclude(username=user.username)
            emailExists = User.objects.filter(
                email=email).exclude(email=user.email)

            if usernameExists:
                messages.error(request, "Username already taken.")
            elif emailExists:
                messages.error(request, "Email already exists.")
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username=username
                user.profile.phone = phone
                user.save()
                user.profile.save()
                messages.success(request, "User details updated")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = UserUpdate()
        form.fields['email'].initial = user.email
        form.fields['first_name'].initial = user.profile.first_name
        form.fields['last_name'].initial = user.profile.last_name
        form.fields['username'].initial = user.username
        form.fields['phone'].initial = user.profile.phone
    return render(request, 'admins/update-user.html', {'form': form, 'user': user})

# delete user


def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, "User has been deleted.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# delete user
def delete_profile(request, id):
    profile = Profile.objects.get(id=id)
    profile.delete()
    messages.success(request, "User has been deleted.")
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
