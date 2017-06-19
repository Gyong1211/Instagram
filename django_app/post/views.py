from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from member.forms import LoginForm
from post.decorators import post_owner
from post.forms import PostForm
from .models import Post, Comment


def post_list(request):
    # 모든 Post목록을 'posts'라는 key로 context에 담아 return render처리
    # post/post_list.html을 template으로 사용하도록 한다

    # 각 포스트에 대해 최대 4개까지의 댓글을 보여주도록 템플릿에 설정
    posts = Post.objects.all()
    loginform = LoginForm()
    context = {
        'posts': posts,
        'loginform': loginform,
    }
    return render(request, 'post/post_list.html', context=context)


def post_detail(request, post_pk):
    loginform = LoginForm()
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
        'loginform': loginform
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
        forms = PostForm()
        context = {
            'form': forms,
        }
        return render(request, 'post/post_create.html', context=context)

@post_owner
@login_required
def post_modify(request, post_pk):
    post = Post.objects.get(id=post_pk)

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
        form.save()
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
    # post_pk에 해당하는 Post에 대한 delete요청만을 받음
    # 처리완료후에는 post_list페이지로 redirect
    post = get_object_or_404(Post, id=post_pk)
    post.delete()
    return redirect('post:post_list')



def comment_create(request, post_pk):
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    pass


def comment_modify(request, post_pk):
    # 수정
    pass


def comment_delete(request, post_pk, comment_pk):
    # POST요청을 받아 Comment객체를 delete, 이후 post_detail페이지로 redirect
    pass
