'''booking views'''
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    '''index view'''
    return render(request, 'index.html')


def service(request):
    '''service view'''
    return render(request, 'service.html')


def contact(request):
    '''contact view'''
    return render(request, 'contact.html')


from django.contrib.auth.decorators import login_required

@login_required
def create_appointment(request):
    '''create appointment view'''
    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            # Check if the selected time slot is already booked for the selected day
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']

            if Appointment.objects.filter(appointment_date=appointment_date,
                                          appointment_time=appointment_time).exists():
                messages.error(
                    request, 'This time slot is already booked. Please select another time slot.')
                return redirect('create_appointment')
            else:
                # Check if the selected choice is in the past
                if appointment_date < datetime.now().date():
                    messages.error(
                        request, 'You cannot select a date in the past.')
                    return redirect('create_appointment')
                else:
                    # Associate the appointment with the currently logged-in user
                    appointment = form.save(commit=False)
                    if not request.user.is_superuser:
                        appointment.customer = request.user
                    appointment.save()
                    messages.success(
                        request, 'Your appointment has been booked.')
                    return redirect('index')
    else:
        form = AppointmentForm()

    return render(request, 'create_appointment.html', {'form': form})



# def appointment_list(request):
#     '''appointment list view'''
#     appointments = Appointment.objects.all()
#     paginator = Paginator(appointments, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     template = 'appointment_list.html'
#     context = {
#         'appointments': page_obj,
#     }
#     return render(request, template, context)



@login_required
def appointment_list(request):
    '''appointment list view'''
    if request.user.is_superuser:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(customer=request.user)

    paginator = Paginator(appointments, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'appointment_list.html'
    context = {
        'appointments': page_obj,
    }
    return render(request, template, context)
