from fastapi import APIRouter

router = APIRouter(prefix="/ping")


@router.get("/db")
def get_db():
    return {"message": "ok"}


@router.post("/app")
def get_app():
    return {"taxt": "app is working"}
