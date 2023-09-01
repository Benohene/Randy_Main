from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('create_appointment/', views.create_appointment,
         name='create_appointment'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
]
