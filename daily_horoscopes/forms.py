from django import forms


class CreateUsersForms(forms.Form):
    email = forms.EmailField(max_length=100, label="Email")
    username = forms.CharField(max_length=100, label="Имя пользователя")
    password = forms.CharField(max_length=100, label="Пароль") # нужно использовать поле passwordInput
