from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label="ПІБ")
    email = forms.EmailField(label="Пошта")
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label="Роль")

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'role', 'password1', 'password2']



class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                if not check_password(password, user.password):
                    raise forms.ValidationError("Неправильний пароль")
                self.user = user
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Користувача з таким email не знайдено")
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


class EnrollInCourseForm(forms.Form):
    code = forms.CharField(max_length=20, label="Course Code")

