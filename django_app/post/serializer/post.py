from rest_framework import serializers

from ..models import Post

__all__ = (
    'PostSerializer'
)


class PostSerializer(serializers.ModelSerializer):
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
