from fastapi import APIRouter, Depends
from database import db_dependency

from typing import List
from utils import *
from schemas import *

router = APIRouter()

@router.post("/")
def create_exercise(exercise: ExerciseCreate, db: db_dependency):
    return create_exercise_in_db(db=db, exercise=exercise)

@router.get("/{session_id}")
def get_session_exercises(session_id: int, db: db_dependency):
    return get_exercises_by_session(db=db, session_id=session_id)


@router.put("/change-workout-exercise/{exercise_id}")
def change_workout_exercise(db: db_dependency, exercise_id: int, change_exercise: WorkoutExerciseChange):
    return change_workout_exercise_in_db(db=db, change_exercise=change_exercise, exercise_id=exercise_id)

@router.delete("/delete-exercise/{exercise_id}")
def delete_exercise(db: db_dependency, exercise_id: int):
    return delete_exercise_in_db(db=db, exercise_id=exercise_id)