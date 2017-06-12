from django import forms


class CreatePost(forms.Form):
    image = forms.ImageField()
    comment = forms.CharField(max_length=100, required=False)


class ModifyPost(forms.Form):
    image = forms.ImageField()