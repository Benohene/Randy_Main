'''Admin View for Appointment'''
from django.contrib import admin
from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    '''Admin View for Appointment'''
    list_display = ('customer', 'name', 'service',
                    'appointment_date', 'appointment_time', 'phone_number', 'message')
    list_filter = ('service', 'appointment_date', 'appointment_time')
    search_fields = ('name', 'phone_number', 'message')
    ordering = ('appointment_date', 'appointment_time')


admin.site.register(Appointment, AppointmentAdmin)
