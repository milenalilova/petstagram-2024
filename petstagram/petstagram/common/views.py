from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


# TODO fix paginator CSS
# TODO fix Search Form
class HomePgeView(ListView):
    model = Photo
    template_name = 'common/home-page.html'
    context_object_name = 'all_photos'  # by default is object_list and photos
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            queryset = queryset.filter(tagged_pets__name__icontains=pet_name)

        return queryset


def like_functionality(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    liked_object = Like.objects.filter(to_photo_id=photo_id, user=request.user).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo=photo, user=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


def copy_link_to_clipboard(request, photo_id):
    copy(request.META.get('HTTP_HOST') + resolve_url('show-photo-details', photo_id))

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


def add_comment(request, photo_id):
    if request.method == "POST":
        photo = Photo.objects.get(id=photo_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')
