from django.urls import path

from users.views import ProfileView, RegisterView, MyLoginView, MyLogoutView, ProfileAvatarView, UserChangePasswordView

app_name = 'users'

urlpatterns = [
    path("api/profile/", ProfileView.as_view({"get": 'retrieve', 'post': 'update'})),
    path("api/profile/avatar/", ProfileAvatarView.as_view({'post': 'update'})),
    path("api/profile/password/", UserChangePasswordView.as_view({'post': 'update'})),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]
