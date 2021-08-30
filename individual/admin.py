from django.contrib import admin

from .models import Individual


class IndividualAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('title',)}
    list_display = ['title', 'doctor', 'category']
    list_filter = ['category']


admin.site.register(Individual, IndividualAdmin)
