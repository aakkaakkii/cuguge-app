from django.urls import path, include

from app.views import views, security


urlpatterns = [
    path('', views.index, name='index'),
    path('post/<post_id>', views.post, name='post'),
    path('createPost', views.create_post, name='createPost'),
    # signup, login & profile
    # path('registration', security.registration, name='registration'),
    # path('account_activation_sent/', security.account_activation_sent, name='account_activation_sent'),
    # path('activate/<uidb64>/<token>/', security.activate, name='activate'),
    # path('accounts/', include('django.contrib.auth.urls'), name='login'),
]

