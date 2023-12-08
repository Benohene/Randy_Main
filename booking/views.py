"""booking views"""
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import (
    AppointmentForm,
    ContactForm,
    ContactReplyForm,
    HolidayForm,
)
from .models import Appointment, Contact, ContactReply, Holiday


def index(request):
    """index view"""
    return render(request, "index.html")


def service(request):
    """service view"""
    return render(request, "service.html")


def contact_view(request):
    """contact view"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get data from the POST request
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone_number = request.POST.get("phone_number")
            message_body = request.POST.get("message_body")

            # Create a Contact object and save it to the database
            contact = Contact.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                message_body=message_body,
                replied=False,
            )

            # Send an email to the owner
            # Replace with the owner's email address
            owner_email = settings.DEFAULT_FROM_EMAIL
            subject = f"New message from {name}"
            message = f"Name: {name}\nEmail: {email}\nPhone Number: {phone_number}\nMessage: {message_body}"
            email_message = EmailMessage(
                subject, message, to=[owner_email]
            )
            email_message.send()

            # Send a confirmation email to the customer
            customer_subject = "Message Received Confirmation"
            customer_message = render_to_string(
                "contact_confirmation_email.html", {"name": name}
            )
            customer_email = EmailMessage(
                customer_subject, customer_message, to=[email]
            )
            customer_email.send()

            # Set replied to True for the contact object
            contact.replied = False
            contact.save()

            # Display a success message
            messages.success(
                request, "Your message has been sent successfully!"
            )
            return redirect("contact")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ContactForm()

    return render(request, "contact_form.html", {"form": form})


@login_required
def reply_to_contact(request, contact_id):
    """reply to contact view"""
    if not request.user.is_superuser:
        messages.error(
            request, "You do not have permission to view this page."
        )
        return redirect("index")
    contact = get_object_or_404(Contact, pk=contact_id)

    if request.method == "POST":
        form = ContactReplyForm(request.POST)
        if form.is_valid():
            reply_text = form.cleaned_data["reply_text"]

            # Create a ContactReply object
            reply = ContactReply(
                contact_message=contact,
                reply_text=reply_text,
                replied_by=request.user,  # Assuming you are using Django's authentication system
                replied=True,
            )
            reply.save()
            # set replied to True for the contact object and save it

            contact.replied = True
            contact.save()

            # Send an email to the original message sender
            send_mail(
                f"Re: Thanks {contact.name}. Reply on your contact with us",
                reply_text,
                settings.DEFAULT_FROM_EMAIL,  # Replace with your email address
                [
                    contact.email
                ],  # Use the email address from the original message
                fail_silently=False,
            )
            messages.success(
                request, "Your reply has been sent successfully!"
            )
            # Redirect to a list of all contact messages
            return redirect("contact_list")

    else:
        form = ContactReplyForm()

    return render(
        request,
        "admin_reply_form.html",
        {"form": form, "contact": contact},
    )


@login_required
def contact_list_view(request):
    """contact list view"""
    if not request.user.is_superuser:
        messages.error(
            request, "You do not have permission to view this page."
        )
        return redirect("index")
    contacts = Contact.objects.all()

    # Sorting
    sort_by = request.GET.get("sort_by", None)
    descending = request.GET.get("descending", False)

    if sort_by:
        if sort_by == "id":
            if descending:
                contacts = contacts.order_by("-id")
            else:
                contacts = contacts.order_by("id")
        elif sort_by == "name":
            if descending:
                contacts = contacts.order_by("-name")
            else:
                contacts = contacts.order_by("name")
        elif sort_by == "email":
            if descending:
                contacts = contacts.order_by("-email")
            else:
                contacts = contacts.order_by("email")
        elif sort_by == "phone_number":
            if descending:
                contacts = contacts.order_by("-phone_number")
            else:
                contacts = contacts.order_by("phone_number")
        elif sort_by == "date":
            if descending:
                contacts = contacts.order_by("-date")
            else:
                contacts = contacts.order_by("date")
        elif sort_by == "replied":
            if descending:
                contacts = contacts.order_by("-replied")
            else:
                contacts = contacts.order_by("replied")

    # Searching
    query = request.GET.get("q", None)
    if query:
        contacts = contacts.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(message_body__icontains=query)
        )

    return render(
        request,
        "contact_list.html",
        {
            "contacts": contacts,
            "sort_by": sort_by,
            "descending": descending,
        },
    )


@login_required
def create_appointment(request):
    """create appointment view"""
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        # check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(
                request, "Please login to book an appointment."
            )
            return redirect("create_appointment")

        if form.is_valid():
            # Check if the selected time slot is already booked for the selected day
            appointment_date = form.cleaned_data["appointment_date"]
            appointment_time = form.cleaned_data["appointment_time"]

            if Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            ).exists():
                messages.error(
                    request,
                    "This time slot is already booked. Please select another time slot.",
                )
                return redirect("create_appointment")
            else:
                # Check if the selected choice is in the past
                if appointment_date < datetime.now().date():
                    messages.error(
                        request, "You cannot select a date in the past."
                    )
                    return redirect("create_appointment")
                else:
                    # Associate the appointment with the currently logged-in user
                    appointment = form.save(commit=False)
                    if not request.user.is_superuser:
                        appointment.customer = request.user
                    appointment.save()
                    messages.success(
                        request, "Your appointment has been booked."
                    )

                    # Send an email to the owner
                    owner_email = (
                        settings.DEFAULT_FROM_EMAIL
                    )  # Replace with the owner's email
                    customer_email = request.user.email
                    subject = "New Appointment Booking"
                    message = f"A new appointment has been booked by {request.user.username} on {appointment_date} at {appointment_time}."
                    send_mail(
                        subject,
                        message,
                        [customer_email],
                        [owner_email],
                        fail_silently=False,
                    )

                    # Send a confirmation email to the customer
                    customer_email = request.user.email
                    subject = "Appointment Confirmation"
                    context = {
                        "user": request.user,
                        "appointment_date": appointment_date,
                        "appointment_time": appointment_time,
                    }
                    html_message = render_to_string(
                        "confirmation_email.html", context
                    )
                    plain_message = strip_tags(html_message)
                    send_mail(
                        subject,
                        plain_message,
                        "randybarber.info@gmail.com",
                        [customer_email],
                        html_message=html_message,
                        fail_silently=False,
                    )

                    # Return to the appointment list after booking
                    return redirect("appointment_list")
    else:
        form = AppointmentForm()

    return render(request, "create_appointment.html", {"form": form})


@login_required
def appointment_list(request):
    """appointment list view"""
    # Get the search query from the request
    search_query = request.GET.get("q", "")

    # Initialize the appointment queryset based on user type
    if request.user.is_superuser:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(customer=request.user)

    # Apply search filter if a search query is provided
    if search_query:
        appointments = appointments.filter(
            Q(customer__username__icontains=search_query)
            | Q(name__icontains=search_query)
            | Q(phone_number__icontains=search_query)
            | Q(message__icontains=search_query)
            | Q(appointment_date__icontains=search_query)
            | Q(appointment_time__icontains=search_query)
        )
        # raise error if no appointment found from search
        if not appointments:
            messages.error(
                request, "No results found matching your query."
            )
            return redirect(reverse("appointment_list"))

    # Sorting logic based on the 'sort' parameter
    sort_by = request.GET.get("sort", "")
    if sort_by == "date_asc":
        appointments = appointments.order_by(
            "appointment_date", "appointment_time"
        )
    elif sort_by == "date_desc":
        appointments = appointments.order_by(
            "-appointment_date", "-appointment_time"
        )
    elif sort_by == "name_asc":
        appointments = appointments.order_by(
            "customer__username", "appointment_date", "appointment_time"
        )
    elif sort_by == "name_desc":
        appointments = appointments.order_by(
            "-customer__username",
            "-appointment_date",
            "-appointment_time",
        )

    paginator = Paginator(appointments, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    template = "appointment_list.html"
    context = {
        "appointments": page_obj,
        "search_query": search_query,
        "sort_by": sort_by,
    }
    return render(request, template, context)


@login_required
def edit_appointment(request, appointment_id):
    """edit appointment view"""
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Check if the user has permission to edit this appointment
    if (
        not request.user.is_superuser
        and appointment.customer != request.user
    ):
        messages.error(
            request,
            "You do not have permission to edit this appointment.",
        )
        return redirect("appointment_list")

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            # Check if the selected time slot is already booked for the selected day
            appointment_date = form.cleaned_data["appointment_date"]
            appointment_time = form.cleaned_data["appointment_time"]

            if (
                Appointment.objects.filter(
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                )
                .exclude(pk=appointment_id)
                .exists()
            ):
                messages.error(
                    request,
                    "This time slot is already booked. Please select another time slot.",
                )
                return redirect("edit_appointment", appointment_id)
            else:
                # Check if the selected choice is in the past
                if appointment_date < datetime.now().date():
                    messages.error(
                        request, "You cannot select a date in the past."
                    )
                    return redirect("edit_appointment", appointment_id)
                else:
                    # Associate the appointment with the currently logged-in user
                    if not request.user.is_superuser:
                        appointment.customer = request.user
                    form.save()
                    messages.success(
                        request, "Your appointment has been updated."
                    )
                    return redirect("appointment_list")
    else:
        form = AppointmentForm(instance=appointment)

    template = "edit_appointment.html"
    context = {
        "form": form,
        "appointment": appointment,
    }
    return render(request, template, context)


# delete appointment view
@login_required
def delete_appointment(request, appointment_id):
    """delete appointment view"""
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Check if the user has permission to delete this appointment
    if (
        not request.user.is_superuser
        and appointment.customer != request.user
    ):
        messages.error(
            request,
            "You do not have permission to delete this appointment.",
        )
        return redirect("appointment_list")

    appointment.delete()
    messages.success(request, "Your appointment has been deleted.")
    return redirect("appointment_list")


def add_holiday(request):
    """add holiday view"""
    holidays = Holiday.objects.all()

    if request.method == "POST":
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Holiday added successfully!")
            return redirect("add_holiday")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = HolidayForm()

    return render(
        request, "add_holiday.html", {"form": form, "holidays": holidays}
    )


def delete_holiday(request, holiday_id):
    """delete holiday item"""
    try:
        holiday = Holiday.objects.get(pk=holiday_id)
        holiday.delete()
        messages.success(request, "Holiday deleted successfully!")
    except Holiday.DoesNotExist:
        messages.error(request, "Holiday not found.")

    return redirect("add_holiday")
