from django.contrib.auth.models import User
from django.db import models


def upload_profile_avatar(instance: 'Profile', filename):
    """
    Получение пути для сохранения изображения профиля
    :param instance: экземпляр профиля
    :param filename: имя файла изображения
    :return: путь для сохранения
    """
    return f'users/avatars/{instance.user.username}/{filename}'


class Profile(models.Model):
    """
    Модель профиля пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles", primary_key=True, verbose_name="пользователь")
    fullName = models.CharField(max_length=128, verbose_name='Ф.И.О.')
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=64, verbose_name='телефон')
    avatar = models.FileField(verbose_name='аватар', upload_to=upload_profile_avatar, blank=True, null=True)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return self.user.username
