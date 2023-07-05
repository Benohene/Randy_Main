from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Appointment)
class Appointment(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "service",
        "day",
        "time",
        "phone_number",
    )
    search_fields = ["name", "day"]
    list_filter = ("time", ("day"))
