from django.shortcuts import render , redirect
from base import models as base_models
from django.contrib.auth.decorators import login_required
from doctor import models as doctor_model
from django.conf import settings
from patient import models as patient_model
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import stripe
from django.http import JsonResponse

# Create your views here.
def index(request):
    service = base_models.Service.objects.all()
    context = {
        "services":service,
    }
    return render(request , "base/index.html" , context=context)

def service_detail(request , service_id):
    services = base_models.Service.objects.get(id=service_id)
    context = {
        "services" : services
    }
    return render(request , "base/service_detail.html",context=context)

@login_required
def book_appointment(request , service_id , doctor_id):
    services = base_models.Service.objects.get(id=service_id)
    doctor =   doctor_model.Doctor.objects.get(id=doctor_id)
    patient = patient_model.Patient.objects.get(user=request.user)
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        # update patient bio data 
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.address = address
        patient.dob = dob
        patient.gender = gender
        patient.save()

        # create appointment object

        appointment = base_models.Appointment.objects.create(
            services=services,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=issues,
            symptoms=symptoms,
            
        )

        # create biling object

        biling = base_models.Billing()
        biling.patient = patient
        biling.appointment = appointment
        biling.sub_total = appointment.services.cost
        biling.tax = appointment.services.cost * 5 / 100
        biling.total = biling.sub_total + biling.tax
        biling.status = "Unpaid"
        biling.save()
        return redirect("base:checkout",biling.biling_id)
    
    context = {
        "services":services,
        "doctor":doctor,
        "patient":patient,
    }

    return render(request,"base/book_appointment.html",context=context)

@login_required
def checkout(request,biling_id):
    biling = base_models.Billing.objects.get(biling_id=biling_id)
    context = {
        "biling":biling,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "stripe_secret_key":settings.STRIPE_SECRET_KEY,
        "pypal_client_id":settings.PYPAL_CLIENT_ID,
    }
    return render(request,"base/checkout.html",context=context)

@csrf_exempt
def stripe_payment(request,biling_id):
    billing = base_models.Billing.objects.get(biling_id=biling_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=billing.patient.email,
        payment_method_type =['card'],
        line_items = [
            {
                'price_date':{
                    'currency':'USD',
                    'product_data':{
                        'name': billing.patient.full_name
                    },
                    'unit_amount': int(billing.total) * 1000
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url = request.build_absolute_url(reverse("base:stripe_payment_verify"),args=[billing.biling_id]) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_url(reverse("base:stripe_payment_verify"),args=[billing.biling_id])
    )
    return JsonResponse({"sessionId": checkout_session.id})


def stripe_payment_verify(request,biling_id):
    biling = base_models.Billing.objects.get(biling_id=biling_id)
    session_id = request.Get.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        if biling.status == "Unpaid":
            biling.status == "Paid"
            biling.save()

            doctor_model.Notification.objects.create(
                doctor=biling.appointment.doctor,
                appointment=biling.appointment,
                type="New Appointment",
            )
            patient_model.Notification.objects.create(
                patient=biling.appointment.patient,
                appointment=biling.appointment,
                type="Appointment Scheduled",
            )

            return redirect(f"/payment_status/{biling.biling_id}/?patment_status=paid")
    else:
        return redirect(f"/payment_status/{biling.biling_id}/?patment_status=failed")

@login_required
def payment_status(request,biling_id):
    biling = base_models.Billing.objects.get(biling_id=biling_id)
    paymet_status = request.GET.get("payment_status")
    
    context = {
        "biling":biling,
        "payment_status":payment_status,
    }

    return render(request,"base/payment_status.html",context=context)