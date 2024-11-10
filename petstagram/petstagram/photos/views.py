from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from petstagram.common.forms import CommentForm
from petstagram.photos.forms import PhotoCreateForm, PhotoEditForm
from petstagram.photos.models import Photo


# def add_photo(request):
#     form = PhotoCreateForm(request.POST, request.FILES)
#     if form.is_valid():
#         form.save()
#         return redirect('home-page')
#     context = {'form': form}
#
#     return render(request, 'photos/photo-add-page.html', context)

class AddPhotoView(CreateView):
    model = Photo
    form_class = PhotoCreateForm
    template_name = 'photos/photo-add-page.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()
        return super().form_valid(form)


def show_photo_details(request, pk):
    photo = Photo.objects.get(pk=pk)
    like = photo.like_set.all()
    comments = photo.comment_set.all()

    comment_form = CommentForm()

    context = {
        'photo': photo,
        'like': like,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'photos/photo-details-page.html', context)


def edit_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    form = PhotoEditForm(request.POST or None, instance=photo)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('show-photo-details', pk)

    context = {
        'form': form,
        'photo': photo
    }

    return render(request, 'photos/photo-edit-page.html', context)


def delete_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    photo.delete()
    return redirect('home-page')
