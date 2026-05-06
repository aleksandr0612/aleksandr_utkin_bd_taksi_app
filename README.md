Projekto paleidimo instrukcija
1. Reikalavimai
Python ≥ 3.11

pip

(nebūtina, bet rekomenduojama) virtuali aplinka venv

Naršyklė (frontend daliai peržiūrėti)

2. Repozitorijos struktūra
text
TAKSI/
├─ backend/
│  ├─ main.py
│  ├─ routers/
│  ├─ models/
│  ├─ ...
├─ frontend/
│  ├─ index.html
│  ├─ app.js
│  ├─ styles.css
3. Backend paleidimas (FastAPI + Uvicorn)
3.1. Virtualios aplinkos sukūrimas (vieną kartą)
bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# arba
source venv/bin/activate  # Linux/Mac
3.2. Priklausomybių įdiegimas
bash
pip install -r requirements.txt
Jei gaunate klaidą No module named 'jose', įsitikinkite, kad python-jose yra requirements.txt ir įdiegtas:

bash
pip install python-jose
3.3. Backend serverio paleidimas
bash
cd backend
venv\Scripts\activate   # jei dar neaktyvuota
python -m uvicorn main:app --reload
Backend pasiekiamas adresu:

text
http://127.0.0.1:8000
4. Frontend paleidimas (statinis SPA)
Frontend dalis yra paprastas HTML + JS + CSS (be npm, be React), todėl ją užtenka patiekti per paprastą HTTP serverį.

4.1. Paleidimas su python -m http.server
bash
cd frontend
python -m http.server 5500
Frontend pasiekiamas adresu:

text
http://127.0.0.1:5500
Svarbu: app.js naudoja API adresą:

js
const API = "http://127.0.0.1:8000";
Todėl backend turi būti paleistas prieš atidarant frontend.

5. Tipinė paleidimo seka
Paleisti backend:

bash
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload
Paleisti frontend:

bash
cd frontend
python -m http.server 5500
Naršyklėje atidaryti:

Frontend: http://127.0.0.1:5500

API dokumentacija (Swagger): http://127.0.0.1:8000/docs
