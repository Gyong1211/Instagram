from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests

from ..decorators import anonymous_required
from ..forms import LoginForm, SignupForm

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
    'facebook_login',
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
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
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
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            django_login(request, user)
            return redirect('post:post_list')

    else:
        pass
    return render(request, 'member/signup.html')


def facebook_login(request):
    code = request.GET.get('code')
    app_access_token = '{}|{}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SECRET_CODE,
    )

    def add_message_and_redirect_referer():
        error_message_for_user = 'Facebook login error'
        messages.error(request, error_message_for_user)
        return redirect(request.META['HTTP_REFERER'])

    def get_access_token(code):
        url_access_token = 'https://graph.facebook.com/v2.9/oauth/access_token'
        redirect_uri = '{}://{}{}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.path,
        )

        url_access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
        }
        response = requests.get(url_access_token, params=url_access_token_params)
        result = response.json()

        if 'access_token' in result:
            return result['access_token']

        elif 'error' in result:
            raise Exception(result['error'])
        else:
            raise Exception('Unknown error')

    if not code:
        return add_message_and_redirect_referer()
    try:
        access_token = get_access_token(code)
    except Exception as e:
        print(e)
        return add_message_and_redirect_referer()
