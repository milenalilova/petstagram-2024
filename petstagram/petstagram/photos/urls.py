from django.urls import path, include

from petstagram.photos import views

urlpatterns = [
path('add/', views.add_photo, name='add-photo'),
    path('<int:pk>/', include(
        [
            path('', views.show_photo_details, name='show-photo-details'),
            path('edit/', views.edit_photo, name='edit-photo'),
            path('delete/', views.delete_photo, name='delete-photo'),
        ]
    )),
]
