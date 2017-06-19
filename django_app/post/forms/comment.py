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

    content = forms.CharField(
        max_length=100,
    )

    class Meta:
        model = Comment
        fields = (
            'content',
        )

    def save(self, **kwargs):
        commit = kwargs.get('commit', True)
        author = kwargs.pop('author', None)
        post = kwargs.pop('post', None)
        comment_pk = kwargs.pop('comment_pk', None)

        if not self.instance.pk or isinstance(author, User):
            self.instance.author = author

        if isinstance(post, Post):
            self.instance.post = post

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
