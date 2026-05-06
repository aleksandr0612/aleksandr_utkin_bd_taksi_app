from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt

from database import get_db
from models import User

SECRET_KEY = "super_secret_key_change_me"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Auth"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # username = email (OAuth2 standarte)
    user = db.query(User).filter(User.email == form_data.username).first()

    # PAPRASTAS SLAPTAŽODŽIO TIKRINIMAS (NE HASH)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Neteisingi duomenys")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }

@router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="El. paštas jau naudojamas")

    # SLAPTAŽODIS SAUGOMAS PAPRASTU TEKSTU (prototipui OK)
    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }
