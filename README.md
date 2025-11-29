# Car Rental Management System

A full-stack car rental management system built with FastAPI, SQLAlchemy, MySQL, React, TypeScript, and Tailwind CSS.

## Features

### Backend (FastAPI)
- **30+ REST API endpoints** with full CRUD operations
- **JWT-based authentication** with role-based access control (Customer, Admin, Clerk)
- **SQLAlchemy ORM** with complete database relationships
- **Pydantic validation** for all API requests
- **Transactional payment processing** with automatic reservation confirmation
- **Business logic services** for pricing, availability, and reservations
- **OOP principles**: Inheritance (User types), Polymorphism (Payment methods), Encapsulation (Reservation state), Abstraction (Service layer)

### Frontend (React + TypeScript)
- **Responsive UI** with Tailwind CSS and shadcn/ui components
- **Role-based dashboards** for customers, admins, and clerks
- **Vehicle browsing** with date-based availability search
- **Reservation workflow** with real-time price calculation
- **Payment processing** integration
- **Customer dashboard** for managing reservations

### Database (MySQL)
- **8 entity tables** with proper relationships and constraints
- **Foreign key constraints** for data integrity
- **Indexes** for optimized queries
- **Check constraints** to prevent overlapping reservations
- **Sample seed data** for testing

## Tech Stack

### Backend
- FastAPI 0.115.5
- SQLAlchemy 2.0.36
- MySQL (via PyMySQL)
- Pydantic 2.10.3
- JWT (python-jose)
- Bcrypt (passlib)

### Frontend
- React 18.3.1
- TypeScript 5.6.3
- Tailwind CSS 3.4.15
- Vite 6.0.1
- React Router 6.28.0
- Axios 1.7.9
- shadcn/ui components

## Project Structure

```
CarRentalManagementSystem/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── auth.py          # Authentication
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   └── main.py          # FastAPI app
│   ├── schema.sql           # Database schema
│   ├── seed_data.sql        # Sample data
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── api/             # API integration
│   │   ├── components/      # Reusable components
│   │   ├── context/         # React context
│   │   ├── pages/           # Page components
│   │   ├── types/           # TypeScript types
│   │   ├── App.tsx          # Main app
│   │   └── main.tsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite configuration
└── README.md                # This file
```

## Database Entities

1. **Users** (with inheritance: Customer, Admin, Clerk)
2. **Locations**
3. **Vehicles**
4. **RatePlans**
5. **Reservations**
6. **Payments**
7. **Inspections**
8. **DamageReports**

## API Endpoints (30+)

### Authentication (3 endpoints)
- POST `/auth/register/customer` - Register new customer
- POST `/auth/register/admin` - Register admin/clerk
- POST `/auth/login` - Login and get JWT token
- GET `/auth/me` - Get current user

### Locations (5 endpoints)
- GET `/locations/` - List all locations
- GET `/locations/{id}` - Get location by ID
- POST `/locations/` - Create location (admin)
- PUT `/locations/{id}` - Update location (admin)
- DELETE `/locations/{id}` - Delete location (admin)

### Vehicles (6 endpoints)
- GET `/vehicles/` - List vehicles with filters
- GET `/vehicles/available` - Get available vehicles by date range
- GET `/vehicles/{id}` - Get vehicle by ID
- GET `/vehicles/{id}/availability` - Check vehicle availability
- POST `/vehicles/` - Create vehicle (admin)
- PUT `/vehicles/{id}` - Update vehicle (admin)
- DELETE `/vehicles/{id}` - Delete vehicle (admin)

### Rate Plans (5 endpoints)
- GET `/rate-plans/` - List all rate plans
- GET `/rate-plans/{id}` - Get rate plan by ID
- POST `/rate-plans/` - Create rate plan (admin)
- PUT `/rate-plans/{id}` - Update rate plan (admin)
- DELETE `/rate-plans/{id}` - Delete rate plan (admin)

### Reservations (8 endpoints)
- GET `/reservations/` - List reservations (role-based)
- GET `/reservations/my-reservations` - Get current user's reservations
- GET `/reservations/{id}` - Get reservation by ID
- POST `/reservations/calculate-price` - Calculate reservation price
- POST `/reservations/` - Create reservation
- PUT `/reservations/{id}` - Update reservation
- POST `/reservations/{id}/activate` - Activate reservation (clerk)
- POST `/reservations/{id}/complete` - Complete reservation (clerk)
- POST `/reservations/{id}/cancel` - Cancel reservation
- DELETE `/reservations/{id}` - Delete reservation (admin/clerk)

### Payments (5 endpoints)
- GET `/payments/` - List payments (role-based)
- GET `/payments/{id}` - Get payment by ID
- GET `/payments/reservation/{id}` - Get payments by reservation
- POST `/payments/` - Create and process payment
- POST `/payments/{id}/refund` - Refund payment (admin)

### Inspections (5 endpoints)
- GET `/inspections/` - List inspections (clerk/admin)
- GET `/inspections/{id}` - Get inspection by ID
- GET `/inspections/reservation/{id}` - Get inspections by reservation
- GET `/inspections/vehicle/{id}` - Get inspections by vehicle
- POST `/inspections/` - Create inspection (clerk/admin)
- PUT `/inspections/{id}` - Update inspection (clerk/admin)
- DELETE `/inspections/{id}` - Delete inspection (admin)

### Damage Reports (5 endpoints)
- GET `/damage-reports/` - List damage reports (clerk/admin)
- GET `/damage-reports/{id}` - Get damage report by ID
- GET `/damage-reports/reservation/{id}` - Get reports by reservation
- GET `/damage-reports/vehicle/{id}` - Get reports by vehicle
- POST `/damage-reports/` - Create damage report (clerk/admin)
- PUT `/damage-reports/{id}` - Update damage report (clerk/admin)
- DELETE `/damage-reports/{id}` - Delete damage report (admin)

**Total: 47 endpoints**

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL 8.0+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
```bash
# Login to MySQL
mysql -u root -p

# Create database
source schema.sql

# Load sample data
source seed_data.sql
```

5. Configure environment variables:
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your MySQL credentials
# DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/car_rental_db
# SECRET_KEY=your-secret-key-here
```

6. Run the backend server:
```bash
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000
API documentation at http://localhost:8000/docs

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Add missing dependency for Tailwind animations:
```bash
npm install tailwindcss-animate
```

4. Run the development server:
```bash
npm run dev
```

Frontend will be available at http://localhost:5173

## Default Test Users

After loading seed data, you can login with:

**Admin:**
- Email: admin@carrental.com
- Password: password123

**Clerk:**
- Email: clerk@carrental.com
- Password: password123

**Customers:**
- Email: john.doe@email.com
- Password: password123

## Business Rules Implemented

1. **Reservation Constraints:**
   - Vehicles cannot have overlapping active reservations
   - End date must be after start date
   - Availability is checked before creating reservations

2. **Pricing Logic:**
   - Base price = daily rate × rental days
   - Discount applied based on rate plan
   - One-way fee added if pickup ≠ dropoff location
   - Insurance calculated per day if selected

3. **Payment Processing:**
   - Payment must succeed before reservation is confirmed
   - Transactional: payment and reservation confirmation happen atomically
   - Vehicle status updated to "reserved" upon payment

4. **Workflow:**
   - Reservation created → Payment processed → Reservation confirmed
   - Clerk activates reservation → Vehicle status = "rented"
   - Clerk completes reservation → Vehicle status = "available"
   - Inspections created on pickup/return
   - Damage reports optional on return

## OOP Principles

### Inheritance
- `User` base class → `Customer`, `Admin`, `Clerk` subclasses

### Polymorphism
- `Payment.process()` method handles different payment methods (card, cash, PayPal)

### Encapsulation
- `Reservation.confirm()`, `activate()`, `complete()`, `cancel()` methods encapsulate state changes

### Abstraction
- Service layer (`PricingService`, `AvailabilityService`, `PaymentService`, `ReservationService`) abstracts business logic from API routes

## License

This is a demonstration project for educational purposes.
