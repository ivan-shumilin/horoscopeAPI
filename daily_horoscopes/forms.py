# from django import forms
#
#
# class CreateUsersForms(forms.Form):
#     email = forms.EmailField(max_length=100, label="Email")
#     username = forms.CharField(max_length=100, label="Имя пользователя",
#                                widget=forms.TextInput(attrs={'class': 'form-input'}))
#     password = forms.CharField(max_length=100, label="Пароль",
#                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
# нужно использовать поле passwordInput
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
