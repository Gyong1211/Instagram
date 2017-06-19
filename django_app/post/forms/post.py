from django import forms

from ..models import Post, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
        if self.instance.my_comment:
            self.fields['comment'].initial = self.instance.my_comment.content

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

    def save(self, **kwargs):
        commit = kwargs.get('commit', True)
        author = kwargs.pop('author', None)

        self.instance.author = author
        instance = super().save(**kwargs)

        comment_string = self.cleaned_data['comment']
        if commit and comment_string:
            if instance.my_comment:
                instance.my_comment.content = comment_string
                instance.my_comment.save()
            else:
                instance.my_comment = Comment.objects.create(
                    post=instance,
                    author=author,
                    content=comment_string
                )
            instance.save()
        return instance


# 내가 쓴거
class CreatePost(forms.Form):
    image = forms.ImageField()
    comment = forms.CharField(max_length=100, required=False)


class ModifyPost(forms.Form):
    image = forms.ImageField()
