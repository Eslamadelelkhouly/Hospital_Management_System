from django.urls import path
from base import views

app_name = "base"

urlpatterns = [
    path("",views.index , name="index"),
    path("service/<service_id>/",views.service_detail , name="service_detail"),
    path("book-appointment/<service_id>/<doctor_id>/",views.book_appointment , name="book_appointment"),
    path("checkout/<biling_id>/",views.checkout , name="checkout"),
    path("payment_status/<biling_id>/",views.payment_status , name="payment_status"),
    path("stripe_payment/<biling_id>/",views.stripe_payment , name="stripe_payment"),
    path("stripe_payment_verify/<biling_id>/",views.stripe_payment_verify , name="stripe_payment_verify"),
]
