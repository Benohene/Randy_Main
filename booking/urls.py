from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact_view, name='contact'),
    path('create_appointment/', views.create_appointment,
         name='create_appointment'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('appointment_edit/<int:appointment_id>/',
         views.edit_appointment, name='edit_appointment'),
    path('appointment_delete/<int:appointment_id>/',
         views.delete_appointment, name='delete_appointment'),
    path('contacts/', views.contact_list_view, name='contact_list'),
    path('contact/<int:contact_id>/',
         views.reply_to_contact, name='reply_to_contact'),
    path('add/', views.add_holiday, name='add_holiday'),
    path('delete/<int:holiday_id>/', views.delete_holiday, name='delete_holiday'),
]
