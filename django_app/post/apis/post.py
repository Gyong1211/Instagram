from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer.post import PostSerializer
from ..models import Post, Comment

__all__ = (
    'PostListCreateView',
)


class PostListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(author=request.user)
            comment_string = request.data.get('comment')
            if comment_string:
                instance.my_comment = Comment.objects.create(
                    post=instance,
                    author=instance.author,
                    content=comment_string
                )
                instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
