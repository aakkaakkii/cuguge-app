from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from app.forms import PostForm, PostImageForm
from app.models import Post, ExtendedUser, PostImage


def index(request):
    post_list = Post.objects.filter(is_shown=True).filter(is_closed=False).order_by('-timestamp')
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        paginator_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginator_queryset = paginator.page(1)
    except EmptyPage:
        paginator_queryset = paginator.page(paginator.num_pages)

    context = {
        'post_list': paginator_queryset,
        'page_request_var': 'page'
    }
    return render(request, 'index.html', context)


def post(request, post_id):
    post_instance = get_object_or_404(Post, id=post_id)

    context = {
        'post': post_instance
    }

    return render(request, 'post.html', context)


@login_required
def create_post(request):
    post_form = PostForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        files = request.FILES.getlist('images')

        if post_form.is_valid():
            p = post_form.save(commit=False)
            p.creator = ExtendedUser.objects.get(user_id=request.user.id)
            p.is_shown = True
            p.save()

            for f in files:
                post_image = PostImage(image=f)
                post_image.save()
                p.images.add(post_image)

            return redirect(reverse('index'))

    context = {
        'post_form': post_form,
    }
    return render(request, 'createPost.html', context)
