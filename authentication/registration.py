from fastapi import HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import *
from .utils import *
# from .. schemas import *
from database import engine, db_dependency
from .scheme import *
from utils import *

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt



Base.metadata.create_all(bind=engine)

router = APIRouter()




        

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register/")
def register_user(user: UserCreate, db: db_dependency):
    # Check if the user with the provided email already exists.
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Pass the entire `user` object to the `create_user` function.
    created_user = create_user(db=db, user=user)
    return created_user

# @router.post("/token")
# def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
#     user = get_user_by_email(db, form_data.username)
#     if not user or not bcrypt.verify(form_data.password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"access_token": user.email, "token_type": "bearer"}



@router.post("/login/")
def login_user(user: UserLogin, db: db_dependency):
    user_db = authenticate_user(db, user.email, user.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": user_db.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password/")
def forgot_password(request: ForgotPassword, db: db_dependency):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )
    # Here you would generate a reset token and send it via email.
    # For simplicity, we return the token.
    reset_token = create_access_token(data={"sub": user.email})
    return {"reset_token": reset_token}




@router.post("/reset-password/")
def reset_password(request: ResetPassword, db: db_dependency):
    payload = decode_access_token(request.token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )
    user_email = payload.get("sub")
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.password = get_hash_password(request.new_password)
    db.commit()
    return {"msg": "Password updated successfully"}