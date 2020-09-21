import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from app.forms import PostForm
from app.models import Post, ExtendedUser, PostImage, PostType, Specie


def index(request):
    post_list = Post.objects.filter(is_shown=True).filter(is_closed=False).order_by('-timestamp')[:3]

    context = {
        'post_list': post_list,
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


@login_required
def edit_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    post_form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == "POST" and instance.creator.user.username == request.user.username:
        files = request.FILES.getlist('images')

        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.save()

            for f in files:
                post_image = PostImage(image=f)
                post_image.save()
                instance.images.add(post_image)

            return redirect('{}/{}'.format(reverse('profile'), '1'))

    context = {
        'post_form': post_form,
        'post_id': post_id,
    }
    return render(request, 'edit_post.html', context)


def profile(request, user_id):
    user = get_object_or_404(ExtendedUser, user_id=user_id)
    post_list = Post.objects.filter(is_shown=True) \
        .filter(is_closed=False).filter(creator=user) \
        .order_by('-timestamp')

    print(user)

    context = {
        'user_info': user,
        'post_list': post_list,
    }

    return render(request, 'profile.html', context)


def posters(request):
    post_list = Post.objects.filter(is_shown=True).filter(is_closed=False)
    filter = {}

    if request.method == "POST":
        if request.POST.get('search'):
            search_word = request.POST.get('search')
            post_list = post_list.filter(Q(title__contains=search_word) | Q(description__contains=search_word)
                                         | Q(post_type__name=search_word) | Q(specie__name=search_word))
        elif request.POST.get('filter'):
            filter = json.loads(request.POST.get('filter'))
            if filter['text']:
                post_list = post_list.filter(
                    Q(title__contains=filter['text']) | Q(description__contains=filter['text']))
            if filter['specie']:
                post_list = post_list.filter(specie_id=filter['post_type'])
            if filter['post_type']:
                post_list = post_list.filter(post_type_id=filter['post_type'])

    post_list = post_list.order_by('-timestamp')

    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    post_types = PostType.objects.all()
    species = Specie.objects.all()

    try:
        paginator_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginator_queryset = paginator.page(1)
    except EmptyPage:
        paginator_queryset = paginator.page(paginator.num_pages)

    context = {
        'post_list': paginator_queryset,
        'page_request_var': 'page',
        'filter': filter,
        'species': species,
        'post_types': post_types
    }
    return render(request, 'posters.html', context)


def load_post_images(request, post_id):
    post_instance = get_object_or_404(Post, id=post_id)
    images = []

    for image in post_instance.images.select_related():
        data = {
            'name': image.image.url,
            'uuid': image.id,
            'thumbnailUrl': image.image.url,
            'size': image.image.size
        }
        images.append(data)

    return JsonResponse(images, safe=False)


@login_required
def delete_image(request, image_id):
    image = PostImage.objects.filter(id=image_id).first()

    if image:
        image.delete()
        return HttpResponse(status=201)
    return HttpResponse(status=201)
