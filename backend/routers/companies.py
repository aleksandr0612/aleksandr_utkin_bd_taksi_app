from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Company, CompanyCity

router = APIRouter(prefix="/companies", tags=["Companies"])


# ============================
# GET ALL COMPANIES
# ============================
@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()

    result = []
    for c in companies:
        cities = db.query(CompanyCity).filter(CompanyCity.company_id == c.id).all()
        city_list = [city.city for city in cities]

        result.append({
            "id": c.id,
            "juridinis_kodas": c.juridinis_kodas,
            "name": c.name,
            "address": c.address,
            "website": c.website,
            "phone_number": c.phone_number,
            "base_price": c.base_price,
            "is_eco": c.is_eco,
            "cities": city_list,
            "butkevicius_score": c.butkevicius_score
        })

    return result


# ============================
# GET COMPANY BY JURIDINIS KODAS
# ============================
@router.get("/by-code/{code}")
def get_company_by_code(code: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.juridinis_kodas == code).first()

    if not company:
        return []  # grąžinam tuščią masyvą, kad frontend nesulūžtų

    cities = db.query(CompanyCity).filter(CompanyCity.company_id == company.id).all()
    city_list = [c.city for c in cities]

    return [{
        "id": company.id,
        "juridinis_kodas": company.juridinis_kodas,
        "name": company.name,
        "address": company.address,
        "website": company.website,
        "phone_number": company.phone_number,
        "base_price": company.base_price,
        "is_eco": company.is_eco,
        "cities": city_list,
        "butkevicius_score": company.butkevicius_score
    }]


# ============================
# GET ALL CITIES
# ============================
@router.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    cities = db.query(CompanyCity.city).distinct().all()
    return [c[0] for c in cities]
