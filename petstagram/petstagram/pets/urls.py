from django.urls import path, include

from petstagram.pets import views

urlpatterns = [
    path('add/', views.add_pet, name='add_pet'),
    path('<str:username>/pet/<slug:pet_slug>/', include(
        [
            path('', views.show_pet_details, name='show_pet_details'),
            path('edit/', views.edit_pet, name='edit_pet'),
            path('delete/', views.delete_pet, name='delete_pet'),
        ]
    ))
]
