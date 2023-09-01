'''booking models'''
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
TIME_CHOICES = (
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)


class Appointment(models.Model):
    '''appointment model'''
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=400, null=True, blank=True)
    appointment_date = models.DateField(default=datetime.now)
    appointment_time = models.CharField(
        max_length=10, choices=TIME_CHOICES, default="")
    phone_number = models.CharField(max_length=20)
    message = models.TextField(null=True, blank=True)

    class Meta:
        '''Meta class'''
        ordering = ['-appointment_date', '-appointment_time']
