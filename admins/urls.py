from django.urls import path

from admins import views

urlpatterns = [
    path('', views.music),
    path('add-music', views.add_music),
    path('my-uploads', views.my_uploads),
    path('update-music/<int:id>', views.update_music),
    path('delete-music/<int:id>', views.delete_music),
    path('add-user/', views.add_user),
    path('users/', views.users),
    path('update-user/<int:id>', views.update_user),
    path('delete-user/<int:id>', views.delete_user),
    path('forgot-password/', views.reset_password),
    path('reset-password/<str:token>', views.change_password),
]