from rest_framework import serializers
from .models import Doctor
from accounts.serializers import UserSerializer


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model."""
    user_email = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'user_email', 'user_name', 'specialization',
            'phone', 'experience_years', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_email(self, obj):
        return obj.user.email
    
    def get_user_name(self, obj):
        return obj.user.name


class DoctorCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Doctor."""
    class Meta:
        model = Doctor
        fields = ['specialization', 'phone', 'experience_years']
