from django.contrib import admin

from app.models import Post, ExtendedUser, Specie, PostType, PostImage

admin.site.register(Post)
admin.site.register(ExtendedUser)
admin.site.register(Specie)
admin.site.register(PostType)
admin.site.register(PostImage)
