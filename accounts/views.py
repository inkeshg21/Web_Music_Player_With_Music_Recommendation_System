from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Profile
from accounts.auth import unauthenticated_user
from accounts.forms import PasswordChange, RegistrationForm, LoginForm


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(
                request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Incorrect Password")
                return render(request, "accounts/login.html", {'form': form})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@unauthenticated_user
def register_user(request):
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
            return redirect('/accounts/login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


def update_profile(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.filter(user=user)
    if not profile:
        profile = Profile.objects.create(user=user)
    else:
        profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        if "details" in request.POST:
            profile.first_name = request.POST.get('first_name')
            profile.last_name = request.POST.get('last_name')
            profile.phone = request.POST.get('phone')
            user.email = request.POST.get('email')
            image = request.FILES.get('image')
            if profile:
                if image:
                    profile.image = image
                profile.save()
                user.save()
                messages.success(request, "Profile updated successfully")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            else:
                messages.success(request, "Profile update failed")
        elif "passwords" in request.POST:
            password_form = PasswordChange(request.POST)
            if password_form.is_valid():
                current_password = password_form.cleaned_data.get('current_password')
                user = auth.authenticate(username=request.user, password=current_password)
                if not user:
                    messages.error(request, "Incorrect password")
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                else:
                    password1 = password_form.cleaned_data.get('password1')
                    profile.user.set_password(password1)
                    profile.user.save()
                    messages.success(request, "Password changed successfully. Please login again")
                    return redirect("/accounts/login")
    else:
        password_form = PasswordChange()
    return render(request, 'accounts/update-profile.html', {'profile': profile, "active_profile": "active", 'form': password_form})


# delete user
def delete_profile(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, "User has been deleted.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
