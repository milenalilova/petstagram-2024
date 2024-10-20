from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


# def index(request):
#     all_photos = Photo.objects.all()
#     comment_form = CommentForm()
#     search_form = SearchForm(request.GET)
#
#     if search_form.is_valid():
#         search_pattern = search_form.cleaned_data['pet_name']
#         if search_pattern:
#             all_photos = all_photos.filter(
#                 tagged_pets__name__icontains=search_form.cleaned_data['pet_name']
#             )
#
#     photos_per_page=1
#     paginator = Paginator(all_photos, photos_per_page)
#     page_number = request.GET.get('page')       # http://localhost:8000/?page=10 => GET {'page': 10}
#
#     all_photos = paginator.get_page(page_number)
#
#     context = {
#         'all_photos': all_photos,
#         'comment_form': comment_form,
#         'search_form': search_form,
#     }
#
#     return render(request, 'common/home-page.html', context)


# TODO fix paginator CSS
# TODO fix Search Form
class HomePgeView(ListView):
    model = Photo
    template_name = 'common/home-page.html'
    context_object_name = 'all_photos'  # by default is object_list and photos
    paginate_by = 1

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
    liked_object = Like.objects.filter(to_photo_id=photo_id).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo=photo)
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
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')
