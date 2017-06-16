from .forms import LoginForm, SignupForm


def forms(requst):
    context = {
        'login_form':LoginForm(),
        'signup_form':SignupForm(),
    }
    return context