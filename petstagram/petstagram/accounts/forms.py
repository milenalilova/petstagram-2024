from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django import forms

from petstagram.accounts.models import Profile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


class AppUserLoginForm(AuthenticationForm):
    email = forms.EmailField()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth', 'profile_picture']
        labels = {
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'date_of_birth': 'Date of Birth:',
            'profile_picture': 'Profile Picture:',
        }
