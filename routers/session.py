from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import db_dependency
from typing import List
from utils import *
from schemas import *

router = APIRouter()

@router.post("/")
def create_session(session: WorkoutSessionCreate, db: db_dependency):
    return create_workout_session(db=db, session=session)

@router.get("/{program_id}")
def get_program_sessions(program_id: int, db: db_dependency):
    return get_sessions_by_program(db=db, program_id=program_id)


@router.put("/change-workout-session/{session_id}")
def change_workout_session(db: db_dependency, session_id: int, change_session: WorkoutSessionChange):
    return change_workout_session_in_db(db=db, change_session=change_session, session_id=session_id)

@router.delete("/delete-session/{session_id}")
def delete_session(db: db_dependency, session_id: int):
    return delete_session_in_db(db=db, session_id=session_id)