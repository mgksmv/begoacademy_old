from django.contrib import admin

from .models import Gallery, PostImage


class PostImageAdmin(admin.StackedInline):
    model = PostImage


@admin.register(Gallery)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('seminar',)}
    inlines = [PostImageAdmin]

    class Meta:
        model = Gallery
