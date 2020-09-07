import os


# signals
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


def auto_delete_images_on_post_delete(sender, instance, **kwargs):
    if instance.images:
        for image in instance.images.all():
            image.delete()
