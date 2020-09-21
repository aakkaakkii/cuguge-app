from django.urls import path, include, re_path

from app.views import views, security


urlpatterns = [
    path('', views.index, name='index'),
    path('posters', views.posters, name='posters'),
    path('post/<post_id>', views.post, name='post'),
    path('createPost', views.create_post, name='createPost'),
    path('editPost/<post_id>', views.edit_post, name='editPost'),
    path('postImages/<post_id>', views.load_post_images, name='postImages'),
    path('deletePostImage/<image_id>/', views.delete_image, name='deletePostImage'),
    path('profile/<user_id>', views.profile, name='profile'),
]

