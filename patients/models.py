from django.db import models


class Patient(models.Model):
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    glucose = models.FloatField()
    haemoglobin = models.FloatField()
    cholesterol = models.FloatField()
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name
