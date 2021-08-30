from django.contrib import admin
from .models import Seminar, Category, OrganizerNumbers, OrganizerWhatsAppNumbers, NewOrganizer, Live, Address

admin.site.site_header = 'BEGO Academy. Админ панель.'


class SeminarAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('title',)}
    list_display = ['title', 'date_info', 'organizer', 'is_finished']
    list_filter = ['date', 'is_finished', 'organizer', 'lector']
    list_editable = ['organizer', 'is_finished', 'date_info']
    search_fields = ['title']
    filter_horizontal = ['category', 'lector']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('category_name',)}


class LiveStatus(admin.ModelAdmin):
    # list_display = ['title', 'video_youtube', 'is_live']
    # list_editable = list_display
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrganizerNumbersAdmin(admin.StackedInline):
    model = OrganizerNumbers
    extra = 1


class OrganizerWhatsAppNumbersAdmin(admin.StackedInline):
    model = OrganizerWhatsAppNumbers
    extra = 1


class LiveAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('title',)}


admin.site.register(Seminar, SeminarAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Live, LiveStatus)
admin.site.register(Address)


@admin.register(NewOrganizer)
class NewOrganizerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}
    inlines = [OrganizerNumbersAdmin, OrganizerWhatsAppNumbersAdmin]

    class Meta:
        model = NewOrganizer
