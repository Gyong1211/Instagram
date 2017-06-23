from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..decorators import anonymous_required
from ..forms import LoginForm, SignupForm

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
)


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
