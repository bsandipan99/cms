from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False, max_length=500)

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        bio = self.cleaned_data.get('bio')

        user = User.objects.create(username=username, password=password)

        Profile.objects.create(user=user, bio=bio)