''' Forms'''
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    '''Appointment form'''
    class Meta:
        '''Meta class'''
        model = Appointment
        fields = ('name', 'service', 'appointment_date', 'appointment_time', 'phone_number', 'message')

        labels = {
            'name': 'Your Name',
            'service': 'Service',
            'appointment_date': 'Date',
            'appointment_time': 'Time',
            'phone_number': 'Phone Number',
            'message': 'Message (Optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add a DateInput widget for the appointment_date field
        self.fields['appointment_date'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'min': str(date.today()),  # Set the minimum date to today
            }
        )

    def clean_appointment_date(self):
        '''Check if the selected date is a Sunday or Monday'''
        appointment_date = self.cleaned_data.get('appointment_date')

        # Check if the selected date is a Sunday or Monday
        if appointment_date and appointment_date.weekday() in [6, 0]:  # Sunday is 6, Monday is 0
            raise ValidationError("Appointments cannot be scheduled on Sundays or Mondays.")

        return appointment_date
