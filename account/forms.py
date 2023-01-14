from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='Email', max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Enter email"}),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Invalid email.',
            'max_length': 'Email must be at most 30 characters.'
        }
    )

    username = forms.CharField(
        label='Username', max_length=15,
        widget=forms.TextInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Enter username"}),
        error_messages={
            'required': 'Username is required.',
            'invalid': 'Invalid username.',
            'max_length': 'Username must be at most 15 characters.',
        }
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Password"})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Retype Password"}))

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('This email is already taken.')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=15,
                               widget=forms.TextInput(
                                   attrs={"class": "form-control form-control-lg rounded text-sm"}),
                               error_messages={
                                   'required': 'Username is required.',
                                   'invalid': 'Invalid username.',
                                   'max_length': 'Username must be at most 15 characters.',
                               })

    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control form-control-lg rounded text-sm"}),
                               error_messages={
                                   'required': 'Password is required.',
                                   'max_length': 'Username must be at most 15 characters.',
                               })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username):
            raise forms.ValidationError('User does not exist.')
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if User.objects.filter(username=username):
            user = auth.authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Incorrect password.')
            return password
