from rest_framework import serializers

from member.serializers.user import UserSerializer
from .comment import CommentSerializer
from ..models import Post

__all__ = (
    'PostSerializer'
)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    my_comment = CommentSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'image',
            'my_comment',
        )
        reads_only_fields = (
            'author',
            'my_comment',
        )
