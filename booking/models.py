'''booking models'''
from datetime import datetime
from django.utils import timezone
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


class Holiday(models.Model):
    '''holiday model'''
    date = models.DateField(default=datetime.now, unique=True)
    name = models.CharField(max_length=400, null=True, blank=True)
    
    class Meta:
        '''Meta class'''
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.name} - {self.date}"


class Contact(models.Model):
    '''contact model'''
    name = models.CharField(max_length=400)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    message_body = models.TextField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)
    replied = models.BooleanField(default=False)

    class Meta:
        '''Meta class'''
        ordering = ['-id', 'replied', 'name']
 

class ContactReply(models.Model):
    '''contact reply model'''
    contact_message = models.ForeignKey(Contact, on_delete=models.CASCADE)
    reply_text = models.TextField()
    reply_date = models.DateTimeField(default=timezone.now)
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    replied = models.BooleanField(default=False)
    
    class Meta:
        '''Meta class'''
        verbose_name_plural = 'Contact Replies'
        ordering = ['-id', 'replied', 'contact_message']
