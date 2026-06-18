#!/usr/bin/env python
"""
Test script for Healthcare Management System API
Tests all endpoints and demonstrates API usage
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_auth():
    """Test authentication endpoints"""
    print("\n\n" + "="*60)
    print("TESTING AUTHENTICATION")
    print("="*60)
    
    # Register
    register_data = {
        "email": "testpatient@example.com",
        "name": "Test Patient",
        "password": "TestPassword123!",
        "password2": "TestPassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    print_response("REGISTER USER", response)
    
    # Login
    login_data = {
        "email": "testpatient@example.com",
        "password": "TestPassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print_response("LOGIN USER", response)
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access']
        return access_token
    return None

def test_patients(access_token):
    """Test patient endpoints"""
    print("\n\n" + "="*60)
    print("TESTING PATIENT ENDPOINTS")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Create patient
    patient_data = {
        "age": 30,
        "gender": "M",
        "blood_group": "O+",
        "phone": "555-0101",
        "address": "123 Main St, New York, NY"
    }
    response = requests.post(f"{BASE_URL}/patients/", json=patient_data, headers=headers)
    print_response("CREATE PATIENT", response)
    
    patient_id = None
    if response.status_code == 201:
        patient_id = response.json()['id']
    
    # List patients
    response = requests.get(f"{BASE_URL}/patients/", headers=headers)
    print_response("LIST PATIENTS", response)
    
    # Get patient
    if patient_id:
        response = requests.get(f"{BASE_URL}/patients/{patient_id}/", headers=headers)
        print_response(f"GET PATIENT {patient_id}", response)
        
        # Update patient
        update_data = {"age": 31, "phone": "555-0102"}
        response = requests.put(f"{BASE_URL}/patients/{patient_id}/", json=update_data, headers=headers)
        print_response("UPDATE PATIENT", response)
    
    return patient_id

def test_doctors(access_token):
    """Test doctor endpoints"""
    print("\n\n" + "="*60)
    print("TESTING DOCTOR ENDPOINTS")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Register doctor user first
    doctor_register_data = {
        "email": "dr.smith@example.com",
        "name": "Dr. Smith",
        "password": "DoctorPassword123!",
        "password2": "DoctorPassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/register/", json=doctor_register_data)
    print_response("REGISTER DOCTOR USER", response)
    
    # Login as doctor to get token
    doctor_login_data = {
        "email": "dr.smith@example.com",
        "password": "DoctorPassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login/", json=doctor_login_data)
    if response.status_code == 200:
        doctor_token = response.json()['access']
        doctor_headers = {"Authorization": f"Bearer {doctor_token}"}
        
        # Create doctor profile
        doctor_data = {
            "specialization": "Cardiologist",
            "phone": "555-0200",
            "experience_years": 10
        }
        response = requests.post(f"{BASE_URL}/doctors/", json=doctor_data, headers=doctor_headers)
        print_response("CREATE DOCTOR", response)
        
        doctor_id = response.json()['id'] if response.status_code == 201 else None
    else:
        doctor_id = None
    
    # List doctors (use original token)
    response = requests.get(f"{BASE_URL}/doctors/", headers=headers)
    print_response("LIST DOCTORS", response)
    
    if doctor_id:
        # Get doctor
        response = requests.get(f"{BASE_URL}/doctors/{doctor_id}/", headers=headers)
        print_response(f"GET DOCTOR {doctor_id}", response)
    
    return doctor_id

def test_mappings(access_token, patient_id, doctor_id):
    """Test mapping endpoints"""
    print("\n\n" + "="*60)
    print("TESTING MAPPING ENDPOINTS")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    if patient_id and doctor_id:
        # Create mapping
        mapping_data = {
            "patient": patient_id,
            "doctor": doctor_id,
            "notes": "Regular checkup scheduled"
        }
        response = requests.post(f"{BASE_URL}/mappings/", json=mapping_data, headers=headers)
        print_response("CREATE MAPPING", response)
        
        mapping_id = response.json()['id'] if response.status_code == 201 else None
        
        # List mappings
        response = requests.get(f"{BASE_URL}/mappings/", headers=headers)
        print_response("LIST MAPPINGS", response)
        
        # Get mappings for patient
        response = requests.get(f"{BASE_URL}/mappings/{patient_id}/", headers=headers)
        print_response(f"GET DOCTORS FOR PATIENT {patient_id}", response)
        
        if mapping_id:
            # Delete mapping
            response = requests.delete(f"{BASE_URL}/mappings/{mapping_id}/", headers=headers)
            print_response("DELETE MAPPING", response)

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("HEALTHCARE MANAGEMENT SYSTEM - API TESTS")
    print("="*60)
    
    # Test authentication
    access_token = test_auth()
    
    if access_token:
        # Test patient endpoints
        patient_id = test_patients(access_token)
        
        # Test doctor endpoints
        doctor_id = test_doctors(access_token)
        
        # Test mapping endpoints
        if patient_id and doctor_id:
            test_mappings(access_token, patient_id, doctor_id)
    
    print("\n\n" + "="*60)
    print("TESTS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()
