from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    juridinis_kodas = Column(String, index=True)
    name = Column(String)
    address = Column(String)
    website = Column(String)
    phone_number = Column(String)
    base_price = Column(Float)
    is_eco = Column(Boolean)

    # PRIDĖTAS LAUKAS — BŪTINA
    butkevicius_score = Column(Float, default=0.0)

    cities = relationship("CompanyCity", back_populates="company")
    reviews = relationship("Review", backref="company")


class CompanyCity(Base):
    __tablename__ = "company_cities"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    city = Column(String)

    company = relationship("Company", back_populates="cities")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    comment = Column(String)
