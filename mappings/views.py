from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PatientDoctorMapping
from patients.models import Patient
from .serializers import PatientDoctorMappingSerializer, PatientDoctorMappingCreateSerializer


class PatientDoctorMappingViewSet(viewsets.ViewSet):
    """ViewSet for PatientDoctorMapping CRUD operations."""
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        """Assign a doctor to a patient."""
        serializer = PatientDoctorMappingCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                mapping = serializer.save()
                return Response(
                    PatientDoctorMappingSerializer(mapping).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """List all mappings."""
        mappings = PatientDoctorMapping.objects.all()
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Get all doctors for a specific patient."""
        try:
            patient = Patient.objects.get(id=pk)
        except Patient.DoesNotExist:
            return Response(
                {'detail': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        """Remove a mapping."""
        try:
            mapping = PatientDoctorMapping.objects.get(id=pk)
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {'detail': 'Mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        mapping.delete()
        return Response(
            {'detail': 'Mapping removed successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
