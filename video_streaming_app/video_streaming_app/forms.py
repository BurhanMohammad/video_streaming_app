from django import forms
from .models import Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class VideoCreationForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_path']