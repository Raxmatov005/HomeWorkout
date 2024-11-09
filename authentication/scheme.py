from pydantic import BaseModel,Field, EmailStr
from fastapi import Depends, HTTPException, status
from models.model import User
from jose import jwt, JWTError
from typing import Optional
from enum import Enum as PyEnum



class GenderEnum(PyEnum):
    male = "male"
    female = "female"
    other = "other"



class WorkoutHistoryEnum(PyEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
        

# User Schemas
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    age: int
    weight: float
    height: float
    goals: str
    gender: GenderEnum  # Use Enum
    workout_history: Optional[WorkoutHistoryEnum]  # Use Enum


class UserLogin(BaseModel):
    email: str
    password: str    



# Password Reset schema
class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str    