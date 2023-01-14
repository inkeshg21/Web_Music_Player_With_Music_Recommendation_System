from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from account.auth import unauthenticated_user
from account.forms import RegistrationForm, LoginForm


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Incorrect Password")
                return render(request, "account/login.html", {'form': form})
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password2')
            user = User.objects.create(username=username, email=email)
            user.set_password(password1)
            user.save()
            return redirect('/account/login')
    else:
        form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
