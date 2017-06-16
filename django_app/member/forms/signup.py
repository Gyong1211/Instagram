from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=20,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Username already exist'
            )
        return username

    # def clean_password1(self):
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #     if password1!=password2:
    #         raise forms.ValidationError(
    #             ''
    #         )
