from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils import *
from schemas import *
from database import db_dependency
from typing import List

router = APIRouter()



@router.post("/")
def post_feedback(feedback: UserFeedbackCreate, db: db_dependency):
    return create_user_feedback(db=db, feedback=feedback)

@router.get("/{session_id}")
def get_feedback_by_session(session_id: int, db: db_dependency):
    return get_feedback_by_session_in_db(db=db, session_id=session_id)
    
@router.delete("/delete-feedback/{feedback_id}")
def delete_feedback(db: db_dependency, feedback_id: int):
    return delete_feedback_in_db(db=db, feedback_id=feedback_id)
