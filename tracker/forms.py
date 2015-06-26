# Copyright 2015 Florian Tautz
# see LICENSE in the project root for licensing information

from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=20)
    email = forms.EmailField(label='E-Mail')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
