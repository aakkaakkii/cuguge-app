from django.contrib.auth import get_user_model
from django.db import models
from tinymce import HTMLField
from django.db.models.signals import post_delete, pre_delete
from .utils import auto_delete_file_on_delete, auto_delete_images_on_post_delete

User = get_user_model()


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # is_editor = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Specie(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PostType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def get_image_filename(instance, filename):
    post_id = instance.post.id
    return "post_images/%s" % post_id


class PostImage(models.Model):
    # image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')
    image = models.ImageField()


class Post(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = HTMLField()
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    creator = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    is_shown = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    images = models.ManyToManyField(PostImage)
    phone = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.title


# signals
post_delete.connect(auto_delete_file_on_delete, sender=PostImage, dispatch_uid="gallery.image.file_cleanup")
pre_delete.connect(auto_delete_images_on_post_delete, sender=Post)
