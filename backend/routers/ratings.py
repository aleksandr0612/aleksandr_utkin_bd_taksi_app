from fastapi import APIRouter

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.get("/")
def get_ratings():
    return {"message": "Ratings endpoint (rezervuota plėtrai)"}
