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
                raise forms.ValidationError('Music is already uploaded')
            return file
