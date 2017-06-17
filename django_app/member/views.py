from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm

User = get_user_model()


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
            loginform = LoginForm()
            context = {
                'login_form':loginform,
            }
            return render(request,'member/login.html', context=context)

    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        loginform = LoginForm()
        context = {
            'login_form':loginform,
        }
        return render(request, 'member/login.html', context=context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        signupform = SignupForm(request.POST)
        if signupform.is_valid():
            user = signupform.create_user()
            django_login(request, user)
            return redirect('post:post_list')


    else:
        signupform = SignupForm()
    context = {
        'signup_form': signupform,
    }
    return render(request, 'member/signup.html', context=context)
