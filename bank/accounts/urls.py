from django.urls import path

from accounts.views import register, user_login, user_logout, profile_view, profile_edit

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/view/', profile_view),
    path('profile/edit/', profile_edit),
]