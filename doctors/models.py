from django.db import models
from accounts.models import User


class Doctor(models.Model):
    """Doctor model linked to User via OneToOne relationship."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    experience_years = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Dr. {self.user.name} ({self.specialization})"
