from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from petstagram.accounts.forms import AppUserCreationForm, ProfileEditForm

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('login')


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'


class AppUserLogoutView(LogoutView):
    pass


def show_profile_details(request, pk):
    return render(request, 'accounts/profile-details-page.html')


# def edit_profile(request, pk):
#     return render(request, 'accounts/profile-edit-page.html')

class ProfileEditView(UpdateView):
    model = UserModel
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={'pk': self.object.pk}
        )


def delete_profile(request, pk):
    return render(request, 'accounts/profile-delete-page.html')
