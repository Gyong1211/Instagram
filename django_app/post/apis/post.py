from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer.post import PostSerializer
from ..models import Post, Comment

__all__ = (
    'PostListCreateView',
    'PostLikeToggleView',
)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        comment_string = self.request.data.get('comment')
        if comment_string:
            instance.my_comment = Comment.objects.create(
                post=instance,
                author=instance.author,
                content=comment_string
            )
            instance.save()


class PostLikeToggleView(APIView):
    def post(self, request, post_pk):
        post_instance = get_object_or_404(Post, pk=post_pk)
        post_like, post_like_created = post_instance.postlike_set.get_or_create(
            user=request.user
        )
        if not post_like_created:
            post_like.delete()
        return Response({'created': post_like_created})