from django.db import models
from django.db.models.signals import post_delete, pre_delete
from tinymce import HTMLField

from app.utils import auto_delete_file_on_delete, auto_delete_images_on_post_delete


class ProductTag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class ProductImage(models.Model):
    # image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')
    image = models.ImageField()


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description = HTMLField()
    tags = models.ManyToManyField(ProductTag)
    is_shown = models.BooleanField(default=True)
    images = models.ManyToManyField(ProductImage)

    def __str__(self):
        return self.title


# signals
post_delete.connect(auto_delete_file_on_delete, sender=ProductImage, dispatch_uid="gallery.product_image.file_cleanup")
pre_delete.connect(auto_delete_images_on_post_delete, sender=Product)

