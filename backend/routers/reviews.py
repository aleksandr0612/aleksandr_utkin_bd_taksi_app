from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Review

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/company/{company_id}")
def get_reviews(company_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.company_id == company_id).all()

@router.post("/")
def create_review(company_id: int, user_id: int, rating: int, comment: str, db: Session = Depends(get_db)):
    review = Review(
        company_id=company_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
