from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import Profile


class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации пользователя на сайте
    """
    fullName = forms.CharField(required=True, label='Ф.И.О.', widget=forms.TextInput)
    phone = forms.CharField(required=True, label='Номер телефона', widget=forms.TextInput)
    password1 = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(required=True, label='Подтвердите пароль', widget=forms.PasswordInput)
    email = forms.CharField(required=True, label='Адрес электронной почты', widget=forms.EmailInput)

    error_messages = {
        "password_mismatch": "Пароли не совпадают! Введите одинаковые пароли!",
        "phone_exists": "Пользователь с таким номером телефона уже существует!",
        "email_exists": "Пользователь с таким email уже существует!",
    }

    class Meta:
        model = User
        fields = ("username", 'fullName', 'email', 'phone', 'password1', 'password2')
        field_classes = {"username": UsernameField}

    def clean_phone(self):
        """
        Определение уникальности номера телефона на сайте
        :return: номер телефона
        """
        phone = self.cleaned_data.get("phone")
        phone_in_db = Profile.objects.filter(phone=phone)
        if phone_in_db:
            raise ValidationError(
                self.error_messages["phone_exists"],
                code="phone_exists",
            )
        return phone

    def clean_email(self):
        """
        Определение уникальности email на сайте
        :return: email address
        """
        email = self.cleaned_data.get("email")
        email_in_db = User.objects.filter(email=email)
        if email_in_db:
            raise ValidationError(
                self.error_messages["email_exists"],
                code="email_exists",
            )
        return email
