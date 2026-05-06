from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_seed = [
    {
        "name": f"User{i}",
        "email": f"user{i}@test.lt",
        "password": "password"   # paprastas tekstas, be hash
    }
    for i in range(1, 6)

]

companies_seed = [
    {
        "juridinis_kodas": "302299878",
        "name": "Bolt Services LT UAB",
        "address": "Lvovo g. 25, Vilnius",
        "website": "https://bolt.eu",
        "phone_number": "+37060000001",
        "base_price": 1.20,
        "is_eco": True,
        "cities": ["Vilnius", "Kaunas", "Klaipėda"]
    },
    {
        "juridinis_kodas": "302409123",
        "name": "eTaksi UAB",
        "address": "Savanorių pr. 123, Kaunas",
        "website": "https://etaksi.lt",
        "phone_number": "+37060000002",
        "base_price": 1.00,
        "is_eco": False,
        "cities": ["Kaunas", "Vilnius"]
    },
    {
        "juridinis_kodas": "301122334",
        "name": "Klaipėdos Taksi UAB",
        "address": "Taikos pr. 10, Klaipėda",
        "website": "https://klaipedostaksi.lt",
        "phone_number": "+37060000003",
        "base_price": 0.95,
        "is_eco": False,
        "cities": ["Klaipėda"]
    },
    {
        "juridinis_kodas": "300998877",
        "name": "Šiaulių Taksi UAB",
        "address": "Tilžės g. 5, Šiauliai",
        "website": "https://siauliutaksi.lt",
        "phone_number": "+37060000004",
        "base_price": 0.90,
        "is_eco": True,
        "cities": ["Šiauliai"]
    },
    {
        "juridinis_kodas": "300776655",
        "name": "Panevėžio Taksi UAB",
        "address": "Respublikos g. 20, Panevėžys",
        "website": "https://paneveziotaksi.lt",
        "phone_number": "+37060000005",
        "base_price": 0.85,
        "is_eco": False,
        "cities": ["Panevėžys"]
    },
]

reviews_seed = [
    {"company_id": 1, "user_id": 1, "rating": 5, "comment": "Labai gerai!"},
    {"company_id": 1, "user_id": 2, "rating": 4, "comment": "Greita kelionė."},
    {"company_id": 2, "user_id": 3, "rating": 3, "comment": "Vidutiniškai."},
    {"company_id": 3, "user_id": 4, "rating": 4, "comment": "Malonus vairuotojas."},
    {"company_id": 4, "user_id": 5, "rating": 5, "comment": "Švarus automobilis."},
]
