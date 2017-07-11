from rest_framework import serializers

from member.serializers.user import UserSerializer
from .comment import CommentSerializer
from ..models import Post

__all__ = (
    'PostSerializer',
)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    my_comment = CommentSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'image',
            'my_comment',
            'comments',
        )
        reads_only_fields = (
            'author',
            'my_comment',
            'comments',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_like'] = self.context['request'].user in instance.like_users.all()
        return ret
