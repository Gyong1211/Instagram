from django import forms
from django.contrib.auth import get_user_model

from ..models import Comment, Post

User = get_user_model()


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = True
        if self.instance.content:
            self.fields['content'].initial = self.instance.content

    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'input-comment',
                    'placeholder': '댓글 입력',
                }
            )
        }

    def save(self, **kwargs):
        commit = kwargs.get('commit', True)
        author = kwargs.pop('author', None)
        post = kwargs.pop('post', None)
        comment_pk = kwargs.pop('comment_pk', None)

        if not self.instance.pk or isinstance(author, User):
            self.instance.author = author

        if isinstance(post, Post):
            self.instance.post = post

        # cleaned_data를 사용하기 위해 views.comment_create에서  form.is_valid()를 써줘야했음
        # 하지만 post_modify에서는 form.is_valid()를 사용하지 않음(why?)

        comment_string = self.cleaned_data['content']
        if commit and comment_string:
            if comment_pk:
                instance = Comment.objects.get(pk=comment_pk)
                instance.content = comment_string
                instance.save()
            else:
                instance = Comment.objects.create(
                    post=self.instance.post,
                    author=self.instance.author,
                    content=comment_string
                )
        return instance
