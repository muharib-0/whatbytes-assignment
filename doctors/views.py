from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Doctor
from .serializers import DoctorSerializer, DoctorCreateUpdateSerializer


class DoctorViewSet(viewsets.ViewSet):
    """ViewSet for Doctor CRUD operations."""
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        """Create a new doctor record."""
        if hasattr(request.user, 'doctor_profile'):
            return Response(
                {'detail': 'User already has a doctor profile'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = DoctorCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save(user=request.user)
            return Response(
                DoctorSerializer(doctor).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """List all doctors."""
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Get a specific doctor."""
        try:
            doctor = Doctor.objects.get(id=pk)
        except Doctor.DoesNotExist:
            return Response(
                {'detail': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        """Update a doctor record."""
        try:
            doctor = Doctor.objects.get(id=pk)
        except Doctor.DoesNotExist:
            return Response(
                {'detail': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = DoctorCreateUpdateSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                DoctorSerializer(doctor).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """Delete a doctor record."""
        try:
            doctor = Doctor.objects.get(id=pk)
        except Doctor.DoesNotExist:
            return Response(
                {'detail': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        doctor.delete()
        return Response(
            {'detail': 'Doctor deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
