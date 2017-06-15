from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model

from django.http import HttpResponse
from django.shortcuts import render, redirect

User = get_user_model()

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            django_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('Login invalid!')


    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        return render(request, 'member/login.html')


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            return HttpResponse('이미 있는 Username입니다.')
        if password1 != password2:
            return HttpResponse('비밀번호 확인이 틀렸습니다.')

        user = User.objects.create_user(
            username=username,
            password=password1
        )
        django_login(request,user)
        return redirect('post:post_list')

    else:
        return render(request, 'member/signup.html')
