from django.shortcuts import render, redirect

from petstagram.photos.forms import PhotoCreateForm
from petstagram.photos.models import Photo


def add_photo(request):
    form = PhotoCreateForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('home-page')
    context = {'form': form}

    return render(request, 'photos/photo-add-page.html', context)


def show_photo_details(request, pk):
    photo = Photo.objects.get(pk=pk)
    like = photo.like_set.all()
    comment = photo.comment_set.all()

    context = {
        'photo': photo,
        'like': like,
        'comment': comment
    }

    return render(request, 'photos/photo-details-page.html', context)


def edit_photo(request, pk):
    return render(request, 'photos/photo-edit-page.html')
