from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from post.decorators import comment_owner
from post.forms import CommentForm
from ..models import Post, Comment

__all__ = (
    'comment_create',
    'comment_modify',
    'comment_delete',
)


@require_POST
@login_required
def comment_create(request, post_pk):
    # post = Post.objects.get(pk=post_pk)
    # form = CommentForm(data=request.POST)
    # user = request.user
    # if form.is_valid():
    #     Comment.objects.create(post=post, author=user, content=form.cleaned_data['content'])
    # return redirect('post:post_detail', post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(data=request.POST)
    next = request.GET.get('next')
    if form.is_valid():
        form.save(
            author=request.user,
            post=post,
        )
        if next:
            return redirect(next)
        return redirect('post:post_detail', post_pk)


@comment_owner
@login_required
def comment_modify(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'POST':
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            form.save(comment_pk=comment_pk)
            return redirect('post:post_detail', post_pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'post/comment_modify.html', context=context)


def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('post:post_detail', post_pk)


