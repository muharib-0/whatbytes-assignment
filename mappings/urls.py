from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientDoctorMappingViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='mapping-list'),
    path('<int:pk>/', views.PatientDoctorMappingViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='mapping-detail'),
]
