from django.shortcuts import render, redirect

from member.models import User
from .forms import CreatePost, ModifyPost
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


def post_create(request):
    if request.method == 'POST':
        forms = CreatePost(request.POST, request.FILES)
        if forms.is_valid():
            user = User.objects.first()
            post = Post.objects.create(author=user, image=request.FILES['image'])
            comment = forms.cleaned_data['comment']
            if not comment == '':
                Comment.objects.create(
                    author=user,
                    post=post,
                    content=comment,
                )
            return redirect('post_list')

        else:
            context = {
                'forms': forms
            }
            return render(request, 'post/post_create.html', context=context)

    elif request.method == 'GET':
        forms = CreatePost()
        context = {
            'forms': forms,
        }
        return render(request, 'post/post_create.html', context=context)

    else:
        forms = CreatePost()
        context = {
            'forms': forms,
        }
        return render(request, 'post/post_create.html', context=context)


def post_modify(request, post_pk):
    post = Post.objects.get(id=post_pk)

    if request.method == 'GET':
        forms = ModifyPost(initial={'image': post.image})
        context = {
            'forms': forms,
            'post': post,
        }
        return render(request, 'post/post_modify.html', context=context)

    elif request.method == 'POST':
        forms = ModifyPost(request.POST, request.FILES)
        if forms.is_valid():
            post.image = request.FILES['image']
            post.save()
            return redirect('post_detail', post_pk=post.id)


