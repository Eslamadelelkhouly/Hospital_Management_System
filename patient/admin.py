from django.contrib import admin
from patient import models


class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'mobile', 'gender', 'dob']  # Updated 'dob'


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'type', 'seen', 'date']  # Updated 'appointment'


admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Notification, NotificationAdmin)
