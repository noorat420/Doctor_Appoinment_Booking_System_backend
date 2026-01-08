# Appointment Booking System - Backend API

A Flask-based REST API for managing doctor appointments, built with clean architecture principles.

## Features

- **Authentication**: JWT-based auth with role-based access (doctor/patient)
- **Doctor Management**: Profile management with designation & specialization
- **Availability**: Doctors can create availability slots
- **Appointments**: Patients can book, view, and cancel appointments
- **Email Notifications**: Confirmation & cancellation emails via Resend

## Tech Stack

- **Framework**: Flask
- **Database**: PostgreSQL (Neon) / SQLite (development)
- **ORM**: SQLAlchemy + Flask-Migrate
- **Auth**: Flask-JWT-Extended
- **Email**: Resend
- **Server**: Gunicorn (production)


## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get JWT token |
| GET | `/auth/me` | Get current user info |

### Doctor
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctor/dashboard` | Doctor dashboard |
| GET | `/doctor/profile` | Get doctor profile |
| POST | `/doctor/profile` | Update doctor profile |
| DELETE | `/doctor/account` | Delete doctor account |
| POST | `/doctor/availability` | Create availability slot |

### Patient
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patient/dashboard` | Patient dashboard |
| GET | `/patient/doctors` | List all doctors (paginated) |
| GET | `/patient/doctors/:id/availability` | Get doctor's available slots |

### Appointments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/appointments` | Book an appointment |
| GET | `/appointments/my` | Get patient's appointments |
| GET | `/appointments/doctor` | Get doctor's appointments |
| POST | `/appointments/:id/cancel` | Cancel an appointment |

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL (or use SQLite for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file:
   ```env
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret
   DATABASE_URL=postgresql://user:pass@host/dbname
   RESEND_API_KEY=your-resend-api-key
   FROM_EMAIL=noreply@yourdomain.com
   DOCTOR_INVITATION_CODE=your-doctor-code
   ```

5. **Run database migrations**
   ```bash
   flask db upgrade
   ```

6. **Start the server**
   ```bash
   # Development
   python app.py
   
   # Production
   gunicorn app:app
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret` |
| `JWT_SECRET_KEY` | JWT signing key | `jwt-dev-secret` |
| `DATABASE_URL` | Database connection URL | `sqlite:///local.db` |
| `RESEND_API_KEY` | Resend API key for emails | - |
| `FROM_EMAIL` | Sender email address | - |
| `DOCTOR_INVITATION_CODE` | Code for doctor registration | `DOC2024SECRET` |

## API Usage Examples

### Register a Patient
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "patient"
  }'
```

### Register a Doctor
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Smith",
    "email": "smith@example.com",
    "password": "password123",
    "role": "doctor",
    "invitation_code": "DOC2024SECRET"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Book Appointment
```bash
curl -X POST http://localhost:5000/appointments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "slot_id": 1
  }'
```

## License

MIT

