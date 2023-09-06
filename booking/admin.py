'''Admin View for Appointment'''
from django.contrib import admin
from .models import Appointment
from .models import Contact, ContactReply


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
    list_display = ('name', 'email', 'phone_number', 'message_body', 'date', 'replied')
    list_filter = ('replied', 'date')
    search_fields = ('name', 'email', 'phone_number', 'message_body', 'date')
    ordering = ('-id', 'replied', 'name')
    

# contact reply admin site
class ContactReplyAdmin(admin.ModelAdmin):
    '''Admin View for ContactReply'''
    list_display = ('contact_message', 'reply_text', 'reply_date', 'replied_by', 'replied')
    list_filter = ('replied', 'reply_date')
    search_fields = ('contact_message', 'reply_text', 'reply_date', 'replied_by')
    ordering = ('-id', 'replied', 'contact_message')


admin.site.register(ContactReply, ContactReplyAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Appointment, AppointmentAdmin)
