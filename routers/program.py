from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db_dependency
from typing import List
from utils import *
from schemas import *




router = APIRouter()

@router.post("/")
def create_program(user_id: int, program: WorkoutProgramCreate, db: db_dependency):
    return create_workout_program(db=db, program=program, user_id=user_id)

@router.get("/{user_id}")
def get_user_programs(user_id: int, db: db_dependency):
    return get_workout_programs_by_user(db=db, user_id=user_id)


@router.put("/change-workout-program/{program_id}")
def change_workout_program(db: db_dependency, program_id: int, change_program: WorkoutProgramChange):
    return change_workout_program_in_db(db=db, change_program=change_program, program_id=program_id)

@router.delete("/delete-program/{program_id}")
def delete_program(db: db_dependency, program_id: int):
    return delete_program_in_db(db=db, program_id=program_id)
