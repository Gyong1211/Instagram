from django.shortcuts import render, redirect

from .forms import CreatePost
from .models import Post, Comment


def post_list(request):
    # 모든 Post목록을 'posts'라는 key로 context에 담아 return render처리
    # post/post_list.html을 template으로 사용하도록 한다

    # 각 포스트에 대해 최대 4개까지의 댓글을 보여주도록 템플릿에 설정
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context=context)


def post_detail(request, post_pk):
    post = Post.objects.get(id=post_pk)
    comments = post.comment_set.all()
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post/post_detail.html', context=context)
