'''Admin View for Appointment'''
from django.contrib import admin
from .models import Appointment
from .models import Contact


class AppointmentAdmin(admin.ModelAdmin):
    '''Admin View for Appointment'''
    list_display = ('customer', 'name',
                    'appointment_date', 'appointment_time', 'phone_number', 'message')
    list_filter = ('appointment_date', 'appointment_time')
    search_fields = ('name', 'phone_number', 'message')
    ordering = ('appointment_date', 'appointment_time')


# contact admin site
class ContactAdmin(admin.ModelAdmin):
    '''Admin View for Contact'''
    list_display = ('name', 'email', 'phone_number', 'message_body', 'replied')
    list_filter = ('replied',)
    search_fields = ('name', 'email', 'phone_number', 'message_body')
    ordering = ('-id', 'replied', 'name')


admin.site.register(Contact, ContactAdmin)
admin.site.register(Appointment, AppointmentAdmin)
