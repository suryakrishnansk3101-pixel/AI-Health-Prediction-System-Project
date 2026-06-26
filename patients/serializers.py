from rest_framework import serializers

from ml.predictor import predict_health_risk
from .models import Patient
from .validators import validate_not_future_date, validate_positive_number


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        error_messages={
            "required": "Full name is required.",
            "blank": "Full name is required.",
        }
    )
    date_of_birth = serializers.DateField(
        error_messages={
            "required": "Date of birth is required.",
            "invalid": "Enter a valid date.",
        }
    )
    email = serializers.EmailField(
        error_messages={
            "required": "Email is required.",
            "blank": "Email is required.",
            "invalid": "Please enter a valid email address.",
        }
    )
    glucose = serializers.FloatField(
        error_messages={
            "required": "Glucose is required.",
            "invalid": "Glucose must be a positive number.",
        }
    )
    haemoglobin = serializers.FloatField(
        error_messages={
            "required": "Haemoglobin is required.",
            "invalid": "Haemoglobin must be a positive number.",
        }
    )
    cholesterol = serializers.FloatField(
        error_messages={
            "required": "Cholesterol is required.",
            "invalid": "Cholesterol must be a positive number.",
        }
    )
    remarks = serializers.CharField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "full_name",
            "date_of_birth",
            "email",
            "glucose",
            "haemoglobin",
            "cholesterol",
            "remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "remarks", "created_at", "updated_at"]

    def validate_full_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Full name is required.")
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters.")
        return value

    def validate_date_of_birth(self, value):
        return validate_not_future_date(value)

    def validate_glucose(self, value):
        return validate_positive_number(value, "Glucose")

    def validate_haemoglobin(self, value):
        return validate_positive_number(value, "Haemoglobin")

    def validate_cholesterol(self, value):
        return validate_positive_number(value, "Cholesterol")

    def _apply_prediction(self, validated_data):
        glucose = validated_data.get("glucose")
        haemoglobin = validated_data.get("haemoglobin")
        cholesterol = validated_data.get("cholesterol")
        validated_data["remarks"] = predict_health_risk(glucose, haemoglobin, cholesterol)
        return validated_data

    def create(self, validated_data):
        return super().create(self._apply_prediction(validated_data))

    def update(self, instance, validated_data):
        glucose = validated_data.get("glucose", instance.glucose)
        haemoglobin = validated_data.get("haemoglobin", instance.haemoglobin)
        cholesterol = validated_data.get("cholesterol", instance.cholesterol)
        validated_data["remarks"] = predict_health_risk(glucose, haemoglobin, cholesterol)
        return super().update(instance, validated_data)
