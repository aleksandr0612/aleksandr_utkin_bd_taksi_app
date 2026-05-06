from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models import Company, CompanyCity, Review, User
from startup_data import companies_seed, reviews_seed, users_seed

# IMPORTAI BE CIKLO
from routers.auth import router as auth_router
from routers.reviews import router as reviews_router
from routers.ratings import router as ratings_router
from routers.companies import router as companies_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            for u in users_seed:
                db.add(User(name=u["name"], email=u["email"], password=u["password"]))
            db.commit()

        if db.query(Company).count() == 0:
            for c in companies_seed:
                company = Company(
                    juridinis_kodas=c["juridinis_kodas"],
                    name=c["name"],
                    address=c["address"],
                    website=c["website"],
                    phone_number=c["phone_number"],
                    base_price=c["base_price"],
                    is_eco=c["is_eco"]
                )
                db.add(company)
                db.commit()
                db.refresh(company)
                for city in c["cities"]:
                    db.add(CompanyCity(company_id=company.id, city=city))
                db.commit()

        if db.query(Review).count() == 0:
            for r in reviews_seed:
                db.add(Review(
                    company_id=r["company_id"],
                    user_id=r["user_id"],
                    rating=r["rating"],
                    comment=r["comment"]
                ))
            db.commit()
    finally:
        db.close()

# REGISTRUOJAM ROUTERIUS
app.include_router(auth_router)
app.include_router(reviews_router)
app.include_router(ratings_router)
app.include_router(companies_router)