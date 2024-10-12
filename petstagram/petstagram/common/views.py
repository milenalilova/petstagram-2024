from django.shortcuts import render

from petstagram.photos.models import Photo


def index(request):
    all_photos = Photo.objects.all()

    context = {'all_photos': all_photos}

    return render(request, 'common/home-page.html', context)
