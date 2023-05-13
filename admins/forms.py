from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from music.models import Music


class MusicForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=500,
        widget=forms.TextInput(
            attrs={"class": "rounded form-control text-s text-secondary", "placeholder": "Music Title"}),
        error_messages={
            'required': 'File is required.',
            'invalid': 'Invalid.'
        }
    )
    file = forms.FileField(
        label='Music file'
    )
    cover = forms.ImageField(
        label='Cover Image',
    )
    poster = forms.ImageField(
        label='Poster Image',
    )

    singer = forms.CharField(
        label='Singer', max_length=250,
        widget=forms.TextInput(
            attrs={"class": "rounded form-control text-s text-secondary", "placeholder": "Enter singer name"}),
        error_messages={
            'required': 'Signer is required.',
            'invalid': 'Invalid .',
            'max_length': 'Singer must be at most 250 characters.',
        }
    )

    duration = forms.CharField(
        label='Duration', max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Enter duration"}),
        error_messages={
            'required': 'Duration is required.',
            'invalid': 'Invalid .',
            'max_length': 'Duration must be at most 50 characters.',
        }
    )

    description = forms.CharField(
        label='Description', max_length=500,
        widget=forms.Textarea(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Enter description"}),
        error_messages={
            'required': 'Description is required.',
            'invalid': 'Invalid .',
            'max_length': 'Description must be at most 500 characters.',
        }
    )

    def clean_file(self):
        if 'file' in self.cleaned_data:
            file = self.cleaned_data['file']
            filter = Music.Objects.filter(file=file)
            if filter:
                #if value chai xa bahan true else false
                raise forms.ValidationError('Music is already uploaded')
            return file


class UserUpdate(forms.Form):
    first_name = forms.CharField(
        label='First Name', max_length=200,
        required= False,
        widget=forms.TextInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Enter first name"}),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Invalid name.',
            'max_length': 'First Name must be at most 200 characters.'
        }
    )
    last_name = forms.CharField(
        label='Last Name', max_length=200,
        required= False,
        widget=forms.TextInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Enter last name"}),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Invalid name.',
            'max_length': 'Last Name must be at most 200 characters.'
        }
    )
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
    phone = forms.CharField(
        label='Phone', max_length=10,
        required= False,
        widget=forms.TextInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Enter phone number"}),
        error_messages={
            'invalid': 'Invalid phone number.',
            'max_length': 'Phone number must be 10 characters.',
        }
    )