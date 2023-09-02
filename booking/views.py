'''booking views'''
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def index(request):
    '''index view'''
    return render(request, 'index.html')


def service(request):
    '''service view'''
    return render(request, 'service.html')


def contact(request):
    '''contact view'''
    return render(request, 'contact.html')


@login_required
def create_appointment(request):
    '''create appointment view'''
    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        # check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to book an appointment.')
            return redirect('create_appointment')

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


@login_required
def appointment_list(request):
    '''appointment list view'''
    # Get the search query from the request
    search_query = request.GET.get('q', '')

    # Initialize the appointment queryset based on user type
    if request.user.is_superuser:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(customer=request.user)

    # Apply search filter if a search query is provided
    if search_query:
        appointments = appointments.filter(
            Q(customer__username__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(appointment_date__icontains=search_query) |
            Q(appointment_time__icontains=search_query)
        )
    # raise error if no appointment found from search
        if not appointments:
            messages.error(request, 'No results found matching your query.')
            return redirect(reverse('appointment_list'))
        

    # Sorting logic based on the 'sort' parameter
    sort_by = request.GET.get('sort', '')
    if sort_by == 'date_asc':
        appointments = appointments.order_by('appointment_date', 'appointment_time')
    elif sort_by == 'date_desc':
        appointments = appointments.order_by('-appointment_date', '-appointment_time')
    elif sort_by == 'name_asc':
        appointments = appointments.order_by('customer__username', 'appointment_date', 'appointment_time')
    elif sort_by == 'name_desc':
        appointments = appointments.order_by('-customer__username', '-appointment_date', '-appointment_time')

    paginator = Paginator(appointments, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'appointment_list.html'
    context = {
        'appointments': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, template, context)


@login_required
def edit_appointment(request, appointment_id):
    '''edit appointment view'''
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Check if the user has permission to edit this appointment
    if not request.user.is_superuser and appointment.customer != request.user:
        messages.error(request, 'You do not have permission to edit this appointment.')
        return redirect('appointment_list')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            # Check if the selected time slot is already booked for the selected day
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']

            if Appointment.objects.filter(appointment_date=appointment_date,
                                          appointment_time=appointment_time).exclude(pk=appointment_id).exists():
                messages.error(
                    request, 'This time slot is already booked. Please select another time slot.')
                return redirect('edit_appointment', appointment_id)
            else:
                # Check if the selected choice is in the past
                if appointment_date < datetime.now().date():
                    messages.error(
                        request, 'You cannot select a date in the past.')
                    return redirect('edit_appointment', appointment_id)
                else:
                    # Associate the appointment with the currently logged-in user
                    if not request.user.is_superuser:
                        appointment.customer = request.user
                    form.save()
                    messages.success(
                        request, 'Your appointment has been updated.')
                    return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    template = 'edit_appointment.html'
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, template, context)


# delete appointment view
@login_required
def delete_appointment(request, appointment_id):
    '''delete appointment view'''
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Check if the user has permission to delete this appointment
    if not request.user.is_superuser and appointment.customer != request.user:
        messages.error(request, 'You do not have permission to delete this appointment.')
        return redirect('appointment_list')

    appointment.delete()
    messages.success(request, 'Your appointment has been deleted.')
    return redirect('appointment_list')
