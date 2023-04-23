from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from accounts.auth import admin_only
from .forms import MusicForm, UserUpdate
from django.shortcuts import render, redirect
from django.contrib import messages
from music.models import Artist, History, Music, Playlist
from accounts.forms import PasswordChange, RegistrationForm
from accounts.models import Profile
from .helpers import send_forgotpassword
import uuid
from django.db.models import Q


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

            user = User.objects.get(id=request.user.id)
            user.is_staff = True
            user.save()

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


@admin_only
def users(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        users = User.objects.filter(
            username__icontains=search)

        context = {
            "users": users,
            'active_users': 'badge-primary text-primary rounded',
            'search': search
        }
    else:
        users = User.objects.filter().exclude(username=request.user)
        context = {
            "users": users,
            'active_users': 'badge-primary text-primary rounded'
        }
    return render(request, 'admins/users.html', context)

# add new user


@admin_only
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
            messages.success(request, "User created successfully")
            return redirect('/admins/add-user')
    else:
        form = RegistrationForm()
    return render(request, 'admins/add-user.html', {'form': form})

# update user


@admin_only
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
                user.profile.first_name = first_name
                user.profile.last_name = last_name
                user.email = email
                print(email)
                user.username = username
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


def artists(request):
    artists = Artist.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        query = Q(first_name=search) | Q(last_name=search)
        artists = Artist.objects.filter(query)
        context = {
            'artists': artists,
            'active_artists': 'badge-primary text-primary rounded'
        }
        return render(request, 'admins/artists.html', context)
    context = {
        'artists': artists,
        'active_artists': 'badge-primary text-primary rounded'
    }
    return render(request, 'admins/artists.html', context)


def add_artist(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        image = request.FILES.get('artist_image')
        artist_exists = Artist.objects.filter(
            first_name=first_name, last_name=last_name).first()
        if (artist_exists):
            messages.error(request, "Artist already added")
            return redirect('/admins/add-artist')
        else:
            artist = Artist.objects.create(
                first_name=first_name, last_name=last_name, image=image)
            artist.save()
            messages.success(request, "Artist added successfully")
            return redirect('/admins/add-artist')
    else:
        return render(request, 'admins/add-artist.html')


def update_artist(request, id):
    artist = Artist.objects.get(id=id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        image = request.FILES.get('artist_image')
        artist_exists = Artist.objects.filter(
            first_name=first_name, last_name=last_name).first()
        if (artist_exists):
            messages.error(request, "Artist already added")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        artist.first_name = first_name
        artist.last_name = last_name
        if image:
            artist.image = image
        artist.save()
        messages.success(request, "Artist details updated")
        return redirect('/admins/add-artist', {'artist': artist})
    else:
        return render(request, 'admins/add-artist.html', {'artist': artist})


def delete_artist(request, id):
    artist = Artist.objects.get(id=id)
    artist.delete()
    messages.success(request, "Artist has been removed.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# reset password


def reset_password(request):
    try:
        if request.method == "POST":
            data = request.POST
            email = data.get('email')
            if not User.objects.filter(email=email).first():
                messages.error(request, "User not found")
            user = User.objects.get(email=email)
            print(user)
            profile = Profile.objects.get(user=user)
            token = str(uuid.uuid4())
            profile.forgot_password_token = token
            profile.save()
            send_forgotpassword(user.email, token)
            messages.success(
                request, "A reset password has been sent to your email")
            return redirect('/admins/forgot-password')
        return render(request, 'admins/forgot-password.html')
    except Exception as e:
        print(e)
        return render(request, 'admins/forgot-password.html')


def change_password(request, token):
    profile = Profile.objects.get(forgot_password_token=token)
    if request.method == "POST":
        form = PasswordChange(request.POST)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user = profile.user
        if user is None:
            messages.error(request, "User not found")
            return redirect(f'/change-password/{token}')
        if password1 != password2:
            messages.error(request, "Password not match")
            return redirect(f'/admins/reset-password/{token}')
        user = User.objects.get(id=user.id)
        user.set_password(password1)
        user.save()
        return redirect('/accounts/login')
    else:
        form = PasswordChange()
    return render(request, 'admins/reset-password.html', {'user_id': profile.user.id, 'form': form})


@ login_required
@ admin_only
def music(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        musics = Music.objects.filter(title__icontains=search)
        context = {
            "musics": musics,
            'active_music': 'badge-primary text-primary rounded',
            'search': search
        }
    else:
        musics = Music.objects.all().order_by('-date')
        context = {
            "musics": musics,
            'active_music': 'badge-primary text-primary rounded'
        }
    return render(request, 'admins/music.html', context)


@ login_required
def my_uploads(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        musics = Music.objects.filter(
            title__icontains=search, uploader=request.user)
        context = {
            "musics": musics,
            'active_uploads': 'badge-primary text-primary rounded',
            'search': search
        }
    else:
        musics = Music.objects.filter(uploader=request.user).order_by('-date')
        context = {
            "musics": musics,
            'active_uploads': 'badge-primary text-primary rounded'
        }
    return render(request, 'admins/music.html', context)
