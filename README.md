# Healthcare Management System - REST API

A comprehensive Django REST Framework backend for managing healthcare data with JWT authentication, patient profiles, doctor records, and patient-doctor mappings.

## 📋 Features

- **Custom User Model** with email-based authentication
- **JWT Authentication** using djangorestframework-simplejwt
- **Patient Management** - User-scoped patient profile creation and management
- **Doctor Management** - Create and manage doctor records
- **Patient-Doctor Mappings** - Assign doctors to patients with notes
- **PostgreSQL** support with SQLite fallback
- **DRF Best Practices** - Serializers, ViewSets, Permission Classes
- **Comprehensive Error Handling** - Meaningful error messages with proper HTTP status codes
- **Admin Panel** - Full Django admin support for all models

## 🏗️ Project Structure

```
healthcare_backend/
├── accounts/           # User authentication and registration
│   ├── models.py       # Custom User model
│   ├── serializers.py  # User serializers
│   ├── views.py        # Auth endpoints
│   └── urls.py         # Auth routes
├── patients/           # Patient management
│   ├── models.py       # Patient model
│   ├── serializers.py  # Patient serializers
│   ├── views.py        # Patient CRUD endpoints
│   └── urls.py         # Patient routes
├── doctors/            # Doctor management
│   ├── models.py       # Doctor model
│   ├── serializers.py  # Doctor serializers
│   ├── views.py        # Doctor CRUD endpoints
│   └── urls.py         # Doctor routes
├── mappings/           # Patient-Doctor relationships
│   ├── models.py       # PatientDoctorMapping model
│   ├── serializers.py  # Mapping serializers
│   ├── views.py        # Mapping CRUD endpoints
│   └── urls.py         # Mapping routes
├── core/               # Project settings and main URLs
│   ├── settings.py     # Django settings with JWT config
│   ├── urls.py         # Main URL configuration
│   └── wsgi.py         # WSGI application
├── manage.py           # Django management script
├── .env.example        # Environment variables template
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (optional, SQLite for development)
- pip or conda

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials and settings.

### 3. Database Setup

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)

For admin panel access:

```bash
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

Server runs at `http://localhost:8000`

## 📡 API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "secure_password123",
  "password2": "secure_password123"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password123"
}
```

**Response (200):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

#### Refresh Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "your-refresh-token"
}
```

---

### Patients

All endpoints require JWT Bearer token: `Authorization: Bearer <access_token>`

#### Create Patient Profile
```http
POST /api/patients/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "age": 30,
  "gender": "M",
  "blood_group": "O+",
  "phone": "123-456-7890",
  "address": "123 Main St, City, State"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user": 1,
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "age": 30,
  "gender": "M",
  "blood_group": "O+",
  "phone": "123-456-7890",
  "address": "123 Main St, City, State",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### List Patient(s)
```http
GET /api/patients/
Authorization: Bearer <access_token>
```

Returns the logged-in user's patient profile (if exists).

#### Get Patient Details
```http
GET /api/patients/{id}/
Authorization: Bearer <access_token>
```

#### Update Patient
```http
PUT /api/patients/{id}/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "age": 31,
  "phone": "987-654-3210"
}
```

#### Delete Patient
```http
DELETE /api/patients/{id}/
Authorization: Bearer <access_token>
```

---

### Doctors

All endpoints require JWT Bearer token.

#### Create Doctor
```http
POST /api/doctors/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "specialization": "Cardiologist",
  "phone": "555-0100",
  "experience_years": 10
}
```

**Response (201):**
```json
{
  "id": 1,
  "user": 1,
  "user_email": "doctor@example.com",
  "user_name": "Dr. Jane Smith",
  "specialization": "Cardiologist",
  "phone": "555-0100",
  "experience_years": 10,
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

#### List All Doctors
```http
GET /api/doctors/
Authorization: Bearer <access_token>
```

#### Get Doctor Details
```http
GET /api/doctors/{id}/
Authorization: Bearer <access_token>
```

#### Update Doctor
```http
PUT /api/doctors/{id}/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "experience_years": 11
}
```

#### Delete Doctor
```http
DELETE /api/doctors/{id}/
Authorization: Bearer <access_token>
```

---

### Patient-Doctor Mappings

All endpoints require JWT Bearer token.

#### Assign Doctor to Patient
```http
POST /api/mappings/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "patient": 1,
  "doctor": 1,
  "notes": "Primary care physician for annual checkup"
}
```

**Response (201):**
```json
{
  "id": 1,
  "patient": 1,
  "doctor": 1,
  "patient_details": {
    "id": 1,
    "user": 1,
    "user_email": "user@example.com",
    "user_name": "John Doe",
    "age": 30,
    "gender": "M",
    "blood_group": "O+",
    "phone": "123-456-7890",
    "address": "123 Main St, City, State",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "doctor_details": {
    "id": 1,
    "user": 1,
    "user_email": "doctor@example.com",
    "user_name": "Dr. Jane Smith",
    "specialization": "Cardiologist",
    "phone": "555-0100",
    "experience_years": 10,
    "created_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  },
  "assigned_at": "2024-01-15T10:40:00Z",
  "notes": "Primary care physician for annual checkup"
}
```

#### List All Mappings
```http
GET /api/mappings/
Authorization: Bearer <access_token>
```

#### Get Doctors for a Patient
```http
GET /api/mappings/{patient_id}/
Authorization: Bearer <access_token>
```

Returns all doctors assigned to the patient.

#### Remove Mapping
```http
DELETE /api/mappings/{id}/
Authorization: Bearer <access_token>
```

---

## 🔐 Authentication

### JWT Token Flow

1. **Register** - Create new user account
2. **Login** - Receive `access` and `refresh` tokens
3. **Use Access Token** - Include in `Authorization: Bearer <access_token>` header
4. **Refresh Token** - When access token expires, use refresh token to get new access token

### Token Lifetime

- **Access Token**: 15 minutes (configurable in `.env`)
- **Refresh Token**: 1 day (configurable in `.env`)

---

## 🎯 Key Design Patterns

### User Scoping
- Patients are scoped to the logged-in user
- Users can only view/edit their own patient profile
- Returns 403 Forbidden for unauthorized access

### Error Handling
- **400 Bad Request** - Invalid input or validation errors
- **401 Unauthorized** - Missing or invalid authentication
- **403 Forbidden** - Authenticated but no permission
- **404 Not Found** - Resource doesn't exist

### Model Relationships
- **User ↔ Patient**: OneToOne (each user can have one patient profile)
- **User ↔ Doctor**: OneToOne (each user can have one doctor profile)
- **Patient ↔ Doctor**: ManyToMany through PatientDoctorMapping

---

## 📝 Models

### User (Custom)
```python
- email (unique, username field)
- name
- password (hashed)
```

### Patient
```python
- user (OneToOne → User)
- age
- gender (choices: M, F, O)
- blood_group (choices: A+, A-, B+, B-, AB+, AB-, O+, O-)
- phone
- address
- created_at
- updated_at
```

### Doctor
```python
- user (OneToOne → User)
- specialization
- phone
- experience_years
- created_at
- updated_at
```

### PatientDoctorMapping
```python
- patient (FK → Patient)
- doctor (FK → Doctor)
- assigned_at
- notes (optional)
- unique_together: (patient, doctor)
```

---

## 🛠️ Configuration

### Database

**SQLite (Development):**
Already configured in `settings.py`.

**PostgreSQL (Production):**
Update `settings.py` DATABASES:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

### JWT Configuration

Edit in `settings.py` SIMPLE_JWT:
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    ...
}
```

---

## 🧪 Testing

### Sample cURL Commands

**Register:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "name": "John Doe",
    "password": "Test@123",
    "password2": "Test@123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "Test@123"
  }'
```

**Create Patient (with token):**
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "age": 30,
    "gender": "M",
    "blood_group": "O+",
    "phone": "123-456-7890",
    "address": "123 Main St"
  }'
```

---

## 📚 Technologies

- **Django 6.0.6** - Web framework
- **Django REST Framework 3.17.1** - REST API toolkit
- **djangorestframework-simplejwt 5.3.2** - JWT authentication
- **PostgreSQL/SQLite** - Database
- **Python 3.9+** - Programming language

---

## 🔄 Development Workflow

```bash
# Activate virtual environment
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows

# Make changes to models
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access admin panel
# http://localhost:8000/admin
```

---

## 📋 Admin Panel

Django admin is fully configured for all models:
- User management
- Patient records
- Doctor records
- Patient-Doctor mappings

Access at `/admin/` after creating a superuser.

---

## 🚨 Important Notes

- **No Session Authentication** - Only JWT is used
- **No Templates** - Pure REST API
- **CSRF Exempt for API** - Not needed for token-based auth
- **Database Migrations** - Always run migrations after model changes
- **Email as Username** - Custom user model uses email instead of username
- **SECRET_KEY** - Change in production via `.env`

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👥 Support

For issues or questions, please refer to the code documentation or create an issue.
