from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import render

from app.forms import PostForm
from app.models import ExtendedUser


# User = get_user_model()


# @receiver(user_signed_up, sender=User)
# def user_sign_up_receiver(request, user, **kwargs):
#     pass


@receiver(pre_social_login)
def pre_social_login_receiver(sender, request, sociallogin, **kwargs):
    user = User.objects.get(username=sociallogin.user)
    ExtendedUser.objects.get_or_create(user_id=user.id, defaults={'user': user})


@login_required
def change_profile(request):
    form = PostForm(request.POST or None, request.FILES or None)

    context = {
        'form': form
    }
    return render(request, 'createPost.html', context)


