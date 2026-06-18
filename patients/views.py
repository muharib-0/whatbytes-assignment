from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer, PatientCreateUpdateSerializer


class PatientViewSet(viewsets.ViewSet):
    """ViewSet for Patient CRUD operations."""
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        """Create a patient profile for the logged-in user."""
        if hasattr(request.user, 'patient_profile'):
            return Response(
                {'detail': 'User already has a patient profile'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = PatientCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save(user=request.user)
            return Response(
                PatientSerializer(patient).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """List patients created by the logged-in user."""
        try:
            patient = request.user.patient_profile
            serializer = PatientSerializer(patient)
            return Response([serializer.data], status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Get a specific patient (must belong to the user)."""
        try:
            patient = Patient.objects.get(id=pk)
        except Patient.DoesNotExist:
            return Response(
                {'detail': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if patient.user != request.user:
            return Response(
                {'detail': 'You do not have permission to access this patient'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        """Update a patient record."""
        try:
            patient = Patient.objects.get(id=pk)
        except Patient.DoesNotExist:
            return Response(
                {'detail': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if patient.user != request.user:
            return Response(
                {'detail': 'You do not have permission to update this patient'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PatientCreateUpdateSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                PatientSerializer(patient).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """Delete a patient record."""
        try:
            patient = Patient.objects.get(id=pk)
        except Patient.DoesNotExist:
            return Response(
                {'detail': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if patient.user != request.user:
            return Response(
                {'detail': 'You do not have permission to delete this patient'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        patient.delete()
        return Response(
            {'detail': 'Patient deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
