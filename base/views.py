from django.shortcuts import render
from base import models as base_models
# Create your views here.
def index(request):
    service = base_models.Service.objects.all()
    context = {
        "services":service
    }
    return render(request , "base/index.html" , context=context)

def service_detail(request , service_id):
    services = base_models.Service.objects.get(id=service_id)
    context = {
        "services" : services
    }
    return render(request , "base/service_detail.html",context=context)