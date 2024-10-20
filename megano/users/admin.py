from django.contrib import admin
from users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Отображение профиля пользователя в административной панели
    """
    model = Profile
