from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

User = get_user_model()

__all__ = (
    'follow_toggle',
    'block_toggle',
)


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
