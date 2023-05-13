from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
import re

class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label='First Name', max_length=200,
        required=False,
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
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Password"})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Retype Password"}))

    # def clean_password1(self):
    #     if 'password1' in self.cleaned_data:
    #         password1 = self.cleaned_data['password1']
    #         if len(password1):
    #             raise forms.ValidationError('Passwords do not match.')
    #         elif password1

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            print(password1)
            print(password2)
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_password1(self):
        if "password1" in self.cleaned_data:
            if(bool(re.search('^[a-zA-Z0-9]*$',self.cleaned_data['password1'])) == True):
                #re.search('^[a-zA-Z0-9]*$' check whether spacial character xa ke nai
                raise forms.ValidationError('Password must contain at least 1 special character and uppercase.')
            else:
                if (len(self.cleaned_data['password1']) < 6):
                    raise forms.ValidationError('Passwords must be more than 6 character.')
                elif (len(self.cleaned_data['password1']) > 18):
                    raise forms.ValidationError('Passwords must be less than 18 character.')
        return self.cleaned_data['password1']

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


class PasswordChange(forms.Form):
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Current Password"}))
    password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "New Password"})
    )
    password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(
            attrs={"class": "form-control rounded text-sm form-control-lg", "placeholder": "Confirm New Password"}))
    def clean_password1(self):
        if "password1" in self.cleaned_data:
            if(bool(re.search('^[a-zA-Z0-9]*$',self.cleaned_data['password1'])) == True):
                raise forms.ValidationError('Password must contain at least 1 special character and uppercase.')
            else:
                if (len(self.cleaned_data['password1']) < 6):
                    raise forms.ValidationError('Passwords must be more than 6 character.')
                elif (len(self.cleaned_data['password1']) > 18):
                    raise forms.ValidationError('Passwords must be less than 18 character.')
        return self.cleaned_data['password1']
    def clean_password2(self):
        # when validation is done all the data is saved in the cleaned dictionary.
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')
