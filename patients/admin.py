from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "glucose",
        "haemoglobin",
        "cholesterol",
        "remarks",
        "created_at",
    )
    search_fields = ("full_name", "email", "remarks")
    list_filter = ("remarks", "created_at")
