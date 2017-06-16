from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=20,
    )
    nickname = forms.CharField(
        max_length=24,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                '사용중인 Username입니다.'
            )
        return username

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname and User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError(
                '사용중인 Nickname입니다.'
            )
        return nickname

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError(
                '비밀번호를 바르게 입력해주세요.'
            )
        return password2

    def create_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password2']
        nickname = self.cleaned_data['nickname']
        user = User.objects.create_user(
            username=username,
            password=password,
            nickname=nickname,
        )
        return user

