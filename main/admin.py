from django.contrib import admin

from .models import Registration, Individual, Lector, ContactUs


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'seminar_name', 'phone_number', 'date_created']
    readonly_fields = ['name', 'seminar_name', 'phone_number', 'date_created']

    def has_add_permission(self, request, obj=None):
        return False


class IndividualAdmin(admin.ModelAdmin):
    list_display = ['name', 'individual_name', 'phone_number', 'date_created']
    readonly_fields = ['name', 'individual_name', 'phone_number', 'date_created']

    def has_add_permission(self, request, obj=None):
        return False


class FormAdmin(admin.ModelAdmin):
    list_display = ['name', 'lector_name', 'phone_number', 'email', 'date_created']
    readonly_fields = ['name', 'lector_name', 'phone_number', 'email', 'date_created']

    def has_add_permission(self, request, obj=None):
        return False


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'date_created']
    readonly_fields = ['name', 'email', 'message', 'date_created']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Individual, IndividualAdmin)
admin.site.register(Lector, FormAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
