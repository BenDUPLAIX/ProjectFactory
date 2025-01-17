from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "is_active", "is_staff", "is_superuser"]