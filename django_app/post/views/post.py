from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_POST

from post.decorators import post_owner
from post.forms import PostForm
from ..models import Post, Tag, PostLike

User = get_user_model()

__all__ = (
    'post_list',
    'post_detail',
    'post_create',
    'post_modify',
    'post_delete',
    'hashtag_post_list',
    'post_like_toggle',
)


def post_list(request):
    # 모든 Post목록을 'posts'라는 key로 context에 담아 return render처리
    # post/post_list.html을 template으로 사용하도록 한다

    # 각 포스트에 대해 최대 4개까지의 댓글을 보여주도록 템플릿에 설정
    if request.user.is_authenticated:
        posts_list = Post.objects.exclude(author__in=request.user.block)
    else:
        posts_list = Post.objects.all()
    p = Paginator(posts_list, 5)

    page = request.GET.get('page')
    try:
        posts = p.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = p.page(p.num_pages)

    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context=context)


def post_detail(request, post_pk):
    try:
        post = Post.objects.get(id=post_pk)
    except Post.DoesNotExist as e:
        # 1. 404 Notfound를 출력한다.
        # return HttpResponseNotFound('Post Not found, detail: {}'.format(e))

        # 2. post_list view로 돌아간다
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)
        # 위 2줄은 return redirect('post:post_list')와 같다.
    template = loader.get_template('post/post_detail.html')

    context = {
        'post': post,
    }
    rendered_string = template.render(context=context, request=request)
    return HttpResponse(rendered_string)
    # return render(request, 'post/post_detail.html', context=context)


@login_required
def post_create(request):
    if request.method == 'POST':
        # forms = CreatePost(request.POST, request.FILES)
        # if forms.is_valid():
        #     user = User.objects.first()
        #     post = Post.objects.create(author=user, image=request.FILES['image'])
        #     comment_string = forms.cleaned_data['comment']
        #     # if not comment_string == '':
        #     #     Comment.objects.create(
        #     #         author=user,
        #     #         post=post,
        #     #         content=comment_string,
        #     #     )
        #     if comment_string:
        #         post.comment_set.create(
        #             author=user,
        #             content=comment_string,
        #         )
        #     return redirect('post:post_list')

        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(
                author=request.user
            )

            # comment_string = form.cleaned_data['comment']
            # if comment_string:
            #     post.comment_set.create(author=request.user, content=comment_string)
            return redirect('post:post_detail', post_pk=post.pk)

        else:
            context = {
                'form': form
            }
            return render(request, 'post/post_create.html', context=context)

    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'post/post_create.html', context=context)


@post_owner
@login_required
def post_modify(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    next = request.GET.get('next')
    # if request.method == 'GET':
    #     forms = ModifyPost(initial={'image': post.image})
    #     context = {
    #         'forms': forms,
    #         'post': post,
    #     }
    #     return render(request, 'post/post_modify.html', context=context)
    #
    # elif request.method == 'POST':
    #     forms = ModifyPost(request.POST, request.FILES)
    #     if forms.is_valid():
    #         post.image = request.FILES['image']
    #         post.save()
    #         return redirect('post:post_detail', post_pk=post.id)
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'post/post_modify.html', context=context)


@post_owner
@login_required
def post_delete(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    post.delete()
    return redirect('post:post_list')


def post_anyway(request):
    return redirect('post:post_list')


def hashtag_post_list(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    # posts = Post.objects.filter(comment__tags=tag) # 모든 댓글에 달린 Tag를 포함해서 검색하는 경우

    posts = Post.objects.filter(my_comment__tags=tag)
    posts_count = posts.count()

    context = {
        'tag': tag,
        'posts': posts,
        'posts_count': posts_count,
    }
    return render(request, 'post/hashtag_post_list.html', context=context)


@require_POST
@login_required
def post_like_toggle(request, post_pk):
    next = request.GET.get('next')
    post = get_object_or_404(Post, pk=post_pk)

    if post.postlike_set.filter(user=request.user).exists():
        postlike = post.postlike_set.filter(user=request.user)
        postlike.delete()

    else:
        PostLike.objects.create(user=request.user, post=post)
    if next:
        return redirect(next)
    return redirect('post:post_detail', post_pk=post.pk)

    # if request.user not in post.like_users.all():
    #     PostLike.objects.create(user=request.user, post=post)
    #     if next:
    #         return redirect(next)
    #     return redirect('post:post_list')
    # else:
    #     postlike = PostLike.objects.get(user=request.user, post=post)
    #     postlike.delete()
    #     if next:
    #         return redirect(next)
    #     return redirect('post:post_list')
