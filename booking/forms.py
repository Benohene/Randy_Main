''' Forms'''
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment
from django.contrib.auth import get_user_model  # Import the user model


class AppointmentForm(forms.ModelForm):
    '''Appointment form'''
    class Meta:
        '''Meta class'''
        model = Appointment
        fields = '__all__' 

        labels = {
            'name': 'Your Name',
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
    
    def clean_appointment_time(self):
        '''Check if the selected time is available'''
        appointment_time = self.cleaned_data.get('appointment_time')
        appointment_date = self.cleaned_data.get('appointment_date')

        # Check if the selected time is available
        if appointment_time and appointment_date:
            # Get all the appointments for the selected date
            appointments = Appointment.objects.filter(appointment_date=appointment_date)

            # Get a list of all the times for the selected date
            times = [appointment.appointment_time for appointment in appointments]

            # Check if the selected time is in the list of times
            if appointment_time in times:
                raise ValidationError("This time is not available. Please select a different time.")

        return appointment_time
    
    def clean(self):
        '''Check if the selected date is in the past'''
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')

        # Check if the selected date is in the past
        if appointment_date and appointment_date < date.today():
            raise ValidationError("Please select a date in the future.")

        return cleaned_data


class ContactForm(forms.Form):
    '''Contact form'''
    name = forms.CharField(max_length=400)
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=20)
    message_body = forms.CharField(widget=forms.Textarea)

    def clean(self):
        '''Check if the email is already in the database'''
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        # Check if the email is already in the database
        if email and get_user_model().objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")

        return cleaned_data
