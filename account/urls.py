from django.urls import path

from account import views

urlpatterns = [
    path('login', views.login_user, name="login"),
    path('register', views.register_user, name="register"),
    path('logout', views.logout_user, name="logout"),
    path('update-profile/<int:id>', views.update_profile, name="update-profile"),
    path('delete-profile/<int:id>', views.delete_profile, name="delete-profile")
]
