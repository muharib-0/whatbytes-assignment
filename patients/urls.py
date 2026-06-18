from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='patient-list'),
    path('<int:pk>/', views.PatientViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='patient-detail'),
]
