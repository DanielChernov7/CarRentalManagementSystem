from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import (
    auth,
    locations,
    vehicles,
    rate_plans,
    reservations,
    payments,
    inspections,
    damage_reports
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Rental Management System",
    description="Full-stack car rental management API with JWT authentication",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(locations.router)
app.include_router(vehicles.router)
app.include_router(rate_plans.router)
app.include_router(reservations.router)
app.include_router(payments.router)
app.include_router(inspections.router)
app.include_router(damage_reports.router)


@app.get("/")
def root():
    return {
        "message": "Car Rental Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
