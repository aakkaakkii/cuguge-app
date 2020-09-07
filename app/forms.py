from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from app.models import Post, ExtendedUser, PostImage
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Post
        fields = ('title', 'description', 'specie', 'post_type')


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", 'first_name', 'last_name', "password1", "password2")


class SimpleSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.save()
        ExtendedUser.objects.create(user=user)
        return user


class PostImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = PostImage
        fields = ('image', )
