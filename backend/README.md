# Car Rental Management System - Backend

FastAPI backend with SQLAlchemy, MySQL, and JWT authentication.

## Quick Start

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up database:
```bash
mysql -u root -p < schema.sql
mysql -u root -p < seed_data.sql
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run server:
```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

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
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/car_rental_db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
