from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

import models
from database import get_db
from schemas import UserCreate, UserResponseSchema

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    t = models.User(**user.model_dump())
    try:
        db.add(t)
        db.commit()
        db.refresh(t)
        print(t)
    except:
        db.rollback()
    return t


@router.get("/get_user", response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    t = db.query(models.User).filter(models.User.id == user_id).first()
    if not t:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return t
