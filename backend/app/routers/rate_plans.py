from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.rate_plan import RatePlan
from app.models.user import User
from app.schemas.rate_plan import RatePlanCreate, RatePlanUpdate, RatePlanResponse
from app.auth import get_current_admin, get_current_user

router = APIRouter(prefix="/rate-plans", tags=["Rate Plans"])


@router.get("/", response_model=List[RatePlanResponse])
def get_all_rate_plans(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    """Get all rate plans"""
    query = db.query(RatePlan)

    if is_active is not None:
        query = query.filter(RatePlan.is_active == is_active)

    rate_plans = query.offset(skip).limit(limit).all()
    return rate_plans


@router.get("/{rate_plan_id}", response_model=RatePlanResponse)
def get_rate_plan(rate_plan_id: int, db: Session = Depends(get_db)):
    """Get rate plan by ID"""
    rate_plan = db.query(RatePlan).filter(RatePlan.id == rate_plan_id).first()
    if not rate_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rate plan not found"
        )
    return rate_plan


@router.post("/", response_model=RatePlanResponse, status_code=status.HTTP_201_CREATED)
def create_rate_plan(
    rate_plan: RatePlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create new rate plan (admin only)"""
    # Check for duplicate name
    existing = db.query(RatePlan).filter(RatePlan.name == rate_plan.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rate plan with this name already exists"
        )

    db_rate_plan = RatePlan(**rate_plan.model_dump())
    db.add(db_rate_plan)
    db.commit()
    db.refresh(db_rate_plan)
    return db_rate_plan


@router.put("/{rate_plan_id}", response_model=RatePlanResponse)
def update_rate_plan(
    rate_plan_id: int,
    rate_plan: RatePlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update rate plan (admin only)"""
    db_rate_plan = db.query(RatePlan).filter(RatePlan.id == rate_plan_id).first()
    if not db_rate_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rate plan not found"
        )

    update_data = rate_plan.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_rate_plan, field, value)

    db.commit()
    db.refresh(db_rate_plan)
    return db_rate_plan


@router.delete("/{rate_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rate_plan(
    rate_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete rate plan (admin only)"""
    db_rate_plan = db.query(RatePlan).filter(RatePlan.id == rate_plan_id).first()
    if not db_rate_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rate plan not found"
        )

    db.delete(db_rate_plan)
    db.commit()
    return None
