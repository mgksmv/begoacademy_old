from django.contrib import admin
from django.utils.html import format_html

from .models import Lector, LectorProfile


class LectorListAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(f'<img src="{object.photo.url}" width="100" />')
    
    thumbnail.short_description = 'Фото'
    
    list_display = ['thumbnail', 'name', 'bio']
    list_display_links = ['thumbnail', 'name']


class LectorAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(f'<img src="{object.photo_1.url}" width="100" />')
        
    thumbnail.short_description = 'Фото'
    
    list_display = ['lector', 'thumbnail']
    list_display_links = ['lector', 'thumbnail']
    
    prepopulated_fields = {'url': ('lector',)}


admin.site.register(Lector, LectorListAdmin)
admin.site.register(LectorProfile, LectorAdmin)
