from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

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


class AppUserDetailView(DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        photos_with_likes = self.object.photo_set.annotate(likes_count=Count('like'))

        context['total_likes_count'] = sum(photo.likes_count for photo in photos_with_likes)
        context['total_pets_count'] = self.object.pet_set.count()
        context['total_photos_count'] = self.object.photo_set.count()

        return context


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


# def delete_profile(request, pk):
#     return render(request, 'accounts/profile-delete-page.html')*
class AppUserDeleteView(DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('home-page')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return redirect(self.get_success_url())
