from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_dependency
from utils import *
from schemas import *

router = APIRouter()


@router.get("/get-user/{user_id}")
def get_user(user_id: int, db: db_dependency):
    return db.query(User).filter(User.id == user_id).first()

# @router.post("/register/")
# def register_user(user: UserCreate, db: db_dependency):
#     db_user = get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return create_user(db=db, user=user)



