from django import forms

from ..models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True

    comment = forms.CharField(
        required=False,
        widget=forms.TextInput
    )
    class Meta:
        model = Post
        fields = (
            'image',
            'comment',
        )






#내가 쓴거
class CreatePost(forms.Form):
    image = forms.ImageField()
    comment = forms.CharField(max_length=100, required=False)


class ModifyPost(forms.Form):
    image = forms.ImageField()