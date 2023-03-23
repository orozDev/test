from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _


class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(required=True, label=_('Имя'),
            widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, label=_('Фамилия'),
            widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label=_('Электронная почта'),
            widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')


class LoginForm(forms.Form):

    username = forms.CharField(label=_('Имя пользователя'), widget=forms.TextInput(
        attrs={'placeholder': 'Введите имя пользователя', 'class': 'input100'}))
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(
        attrs={'placeholder': 'Введите пароль', 'class': 'input100'}))


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs=
                                                              {'placeholder': 'Придумайте пароль', 'class': 'input100'})
        self.fields['password2'].widget = forms.PasswordInput(attrs=
                                                              {'placeholder': 'Подтвердите пароль', 'class': 'input100'})

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

        widgets = {
            'username': forms.TextInput(attrs=
                                     {'placeholder': 'Придумайте имя пользователя', 'class': 'input100'}),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Введите имя', 'class': 'input100'}),
            'last_name': forms.TextInput(attrs=
                                         {'placeholder': 'Введите фамилию', 'class': 'input100'}),
            'email': forms.EmailInput(attrs=
                                      {'placeholder': 'Введите почту', 'class': 'input100'}),
        }