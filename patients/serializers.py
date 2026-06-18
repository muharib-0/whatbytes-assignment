from rest_framework import serializers
from .models import Patient
from accounts.serializers import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model."""
    user_email = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'user_email', 'user_name', 'age', 'gender',
            'blood_group', 'phone', 'address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_user_email(self, obj):
        return obj.user.email
    
    def get_user_name(self, obj):
        return obj.user.name


class PatientCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Patient."""
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'blood_group', 'phone', 'address']
