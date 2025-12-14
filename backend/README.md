# Car Rental Management System - Backend

FastAPI backend with SQLAlchemy, PostgreSQL, and JWT authentication.

## Quick Start

### 1. Start PostgreSQL Database

From project root:
```bash
docker-compose up -d
```

This starts PostgreSQL on port 5432 with credentials:
- User: `admin`
- Password: `admin123`
- Database: `car_rental_db`

### 2. Set Up Python Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Update `.env` if needed (default settings work with docker-compose).

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Seed Database (Optional)

```bash
python seed.py
```

This creates test data including:
- Admin user: `admin@carrental.com` / `password123`
- Clerk user: `clerk@carrental.com` / `password123`
- Customer: `john.doe@email.com` / `password123`

### 6. Start Server

```bash
uvicorn app.main:app --reload
```

Server runs on http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Project Structure

```
app/
├── models/          # SQLAlchemy ORM models
│   ├── user.py
│   ├── location.py
│   ├── vehicle.py
│   ├── rate_plan.py
│   ├── reservation.py
│   ├── payment.py
│   ├── inspection.py
│   └── damage_report.py
├── schemas/         # Pydantic validation schemas
├── routers/         # API endpoint routers
├── services/        # Business logic services
│   ├── pricing_service.py
│   ├── availability_service.py
│   ├── payment_service.py
│   └── reservation_service.py
├── auth.py          # Authentication & authorization
├── config.py        # Configuration settings
├── database.py      # Database connection
└── main.py          # FastAPI application
```

## Database Models

All models implement proper OOP principles:

- **Inheritance**: User → Customer/Admin/Clerk
- **Encapsulation**: Reservation state management methods
- **Polymorphism**: Payment processing interface
- **Abstraction**: Service layer separates business logic

## API Features

- JWT-based authentication
- Role-based access control
- Automatic request validation
- Transactional operations
- Comprehensive error handling
- API documentation with Swagger/OpenAPI

## Environment Variables

```
DATABASE_URL=postgresql://admin:admin123@localhost:5432/car_rental_db
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Management

### Create New Migration
```bash
alembic revision --autogenerate -m "description"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

### Stop Database
```bash
docker-compose down
```

### Reset Database (Warning: Deletes All Data)
```bash
docker-compose down -v
docker-compose up -d
alembic upgrade head
python seed.py
```
