from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


def login(request):
    if request.method == 'POST':
        username = request.POST['username'],
        password = request.POST['password'],
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
        if request.user.is_autenticated:
            return redirect('post:post_list')
        return render(request, 'member/login.html')
