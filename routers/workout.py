from fastapi import APIRouter, Depends
from schemas import *
from database import *
from sqlalchemy.orm import Session
from utils import *
from models.model import *

router = APIRouter()


# Route to create a new workout category
@router.post("/create-workout-category")
def create_workout_category(category: WorkoutCategoryCreate, db: db_dependency):
    # Check if the category already exists by its name
    existing_category = get_workout_category_by_name(db=db, category_name=category.category_name)
    if existing_category:
        raise HTTPException(status_code=403, detail="This category already exists")
    
    # Create the workout category
    return create_category_in_db(db=db, category=category)
@router.get("/get-workout-category")
def get_workout_category(db: db_dependency, category_name: str):
    return get_workout_category_by_name(db=db, category_name=category_name)

@router.put("/change-workout-category/{category_id}")
def change_workout_category(db: db_dependency, category_id: int, change_category: WorkoutCategoryChange):
    return change_workout_category_in_db(db=db, change_category=change_category, category_id=category_id)



