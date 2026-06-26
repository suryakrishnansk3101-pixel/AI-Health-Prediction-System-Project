import math

from django.utils import timezone
from rest_framework import serializers


def validate_not_future_date(value):
    if value > timezone.localdate():
        raise serializers.ValidationError("Date of birth cannot be a future date.")
    return value


def validate_positive_number(value, field_name):
    if value is None:
        raise serializers.ValidationError(f"{field_name} is required.")
    if not isinstance(value, (int, float)) or math.isnan(value) or value <= 0:
        raise serializers.ValidationError(f"{field_name} must be a positive number.")
    return value
