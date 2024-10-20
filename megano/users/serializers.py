from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализация профиля пользователя
    """

    class Meta:
        model = Profile
        fields = ['fullName', 'phone', 'email', 'avatar']


class ProfileAvatarSerializer(serializers.ModelSerializer):
    """
    Сериализация аватара пользователя
    """

    class Meta:
        model = Profile
        fields = ['avatar']


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Сериализация пароля пользователя
    """

    class Meta:
        model = User
        fields = ['password']
