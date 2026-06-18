from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """Serializer for PatientDoctorMapping model."""
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_details', 'doctor_details',
            'assigned_at', 'notes'
        ]
        read_only_fields = ['id', 'assigned_at']


class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating PatientDoctorMapping."""
    class Meta:
        model = PatientDoctorMapping
        fields = ['patient', 'doctor', 'notes']
