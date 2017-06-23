from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .decorators import anonymous_required
from .forms import LoginForm, SignupForm, UserEditForm

User = get_user_model()


@anonymous_required
def login(request):
    if request.method == 'POST':
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(
        #     username=username,
        #     password=password
        # )
        # if user is not None:
        #     django_login(request, user)
        #     return redirect('post:post_list')
        # else:
        #     return HttpResponse('Login invalid!')
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            user = loginform.cleaned_data['user']
            django_login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_list')

    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
    return render(request, 'member/login.html')


@login_required
def logout(request):
    django_logout(request)
    return redirect('post:post_list')


@anonymous_required
def signup(request):
    if request.method == 'POST':
        signupform = SignupForm(request.POST)
        if signupform.is_valid():
            user = signupform.create_user()
            django_login(request, user)
            return redirect('post:post_list')

    else:
        pass
    return render(request, 'member/signup.html')


def profile(request, user_pk=None):
    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user

    page = request.GET.get('page', 1)
    post_per_page = 3
    post_num = user.post_set.count()
    if post_num % post_per_page:
        page_num = post_num // post_per_page + 1
    else:
        page_num = post_num // post_per_page
    post_list = user.post_set.all().order_by('-created_date')

    try:
        page = int(page)
    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print(e)

    if page < 1:
        page = 1
    elif page > page_num:
        page = page_num
    else:
        pass
    posts = post_list[:(page * post_per_page)]
    last_post_pk = posts.last().pk

    context = {
        'cur_user': user,
        'posts': posts,
        'next_page_num': page + 1,
        'max_page_num': page_num,
        'last_post_pk': last_post_pk
    }
    return render(request, 'member/profile.html', context=context)


@require_POST
@login_required
def follow_toggle(request, user_pk):
    target_user = get_object_or_404(User, pk=user_pk)
    request.user.follow_toggle(target_user)
    next = request.GET.get('next')
    if next:
        return redirect(next)
    return redirect('my_profile')


@require_POST
@login_required
def block_toggle(request, user_pk):
    target_user = get_object_or_404(User, pk=user_pk)
    request.user.block_toggle(target_user)
    next = request.GET.get('next')
    if next:
        return redirect(next)
    return redirect('my_profile')


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('member:my_profile')
    else:
        form = UserEditForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'member/profile_edit.html', context=context)
