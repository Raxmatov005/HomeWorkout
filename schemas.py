from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.model import *
import enum
from sqlalchemy import Enum


##################################################    ENUMS    ################################################################



class GenderEnum(enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'


class WorkoutHistoryEnum(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class ProgressEnum(enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"

class GoalEnum(enum.Enum):
    weight_loss = "weight_loss"
    muscle_gain = "muscle_gain"
    endurance = "endurance"

class DifficultyEnum(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class TargetMuscleEnum(enum.Enum):
    chest = "chest"
    back = "back"
    arms = "arms"
    legs = "legs"
    core = "core"

class FeedbackTypeEnum(enum.Enum):
    positive = "positive"
    negative = "negative"
    ignore = "ignore"

class PositiveFeedbackEnum(enum.Enum):
    effective = "effective"
    motivating = "motivating"
    enjoyable = "enjoyable"
    other = "other"

class NegativeFeedbackEnum(enum.Enum):
    too_difficult = "too_difficult"
    too_easy = "too_easy"
    unmotivating = "unmotivating"
    other = "other"


##################################################    PASSWORD CHANGE    ################################################################


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


##################################################    USER    ################################################################

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



    class Config:
        arbitrary_types_allowed = True
        from_attributes = True  # Pydantic v2 rename

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int
    weight: float
    height: float
    gender: str
    activity_level: str
    goals: str
    workout_history: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


##################################################   WORKOUT CATEGORY    ################################################################

# Workout Category Schemas
class WorkoutCategoryCreate(BaseModel):
    category_name: str
    description: str
    recommended_frequency: int

    class Config:
        from_attributes = True

class WorkoutCategoryChange(BaseModel):
    category_name: str
    description: str
    recommended_frequency: int

    class Config:
        from_attributes = True


##################################################    WORKOUT PROGRAM    ################################################################

# Workout Program Schemas
class WorkoutProgramCreate(BaseModel):
    frequency_per_week: int
    total_duration: int
    progress: ProgressEnum  # Use Enum
    overall_goal: GoalEnum  # Use Enum
    workout_category_id: int
    start_date: datetime
    end_date: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class WorkoutProgramResponse(BaseModel):
    frequency_per_week: int
    total_duration: int
    progress: ProgressEnum  # Use Enum
    overall_goal: GoalEnum  # Use Enum
    workout_category_id: int
    start_date: datetime
    end_date: datetime
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class WorkoutProgramChange(BaseModel):
    frequency_per_week: int
    total_duration: int
    progress: ProgressEnum  # Use Enum
    overall_goal: GoalEnum  # Use Enum
    active: bool
    start_date: datetime
    end_date: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


##################################################   WORKOUT SESSION    ################################################################

# Workout Session Schemas
class WorkoutSessionCreate(BaseModel):
    program_id: int
    completion_status: bool
    user_feedback: Optional[str]
    performance_notes: Optional[str]
    calories_burned: Optional[float]
    actual_date: Optional[datetime]
    scheduled_date: datetime

    class Config:
        from_attributes = True

class WorkoutSessionResponse(BaseModel):
    program_id: int
    completion_status: bool
    user_feedback: Optional[str]
    performance_notes: Optional[str]
    calories_burned: Optional[float]
    actual_date: Optional[datetime]
    scheduled_date: datetime

    class Config:
        from_attributes = True



class WorkoutSessionChange(BaseModel):
    completion_status: bool 
    user_feedback: str 
    performance_notes: str 
    calories_burned: float 
    actual_date: datetime 
    scheduled_date: datetime 


    class Config:
        from_attributes = True


##################################################    WORKOUT EXERCISE    ################################################################

# Exercise Schemas
class ExerciseCreate(BaseModel):
    session_id: int
    name: str
    description: str
    difficulty_level: DifficultyEnum  # Use Enum
    duration: int  # in minutes
    calories_burned: float
    category_id: int
    video_url: str
    target_muscle: TargetMuscleEnum  # Use Enum

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class ExerciseResponse(BaseModel):
    session_id: int
    name: str
    description: str
    difficulty_level: DifficultyEnum  # Use Enum
    duration: int
    calories_burned: float
    video_url: str
    target_muscle: TargetMuscleEnum  # Use Enum

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class WorkoutExerciseChange(BaseModel):
    name: str
    description: str
    difficulty_level: DifficultyEnum  # Use Enum
    duration: int
    calories_burned: float
    video_url: str
    target_muscle: TargetMuscleEnum  # Use Enum

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


##################################################    USER FEEDBACK    ################################################################

# User Feedback Schemas
class UserFeedbackCreate(BaseModel):
    session_id: int
    user_id: int
    feedback_type: FeedbackTypeEnum
    positive_feedback: Optional[PositiveFeedbackEnum] = None  # Only if feedback_type is positive
    negative_feedback: Optional[NegativeFeedbackEnum] = None  # Only if feedback_type is negative
    additional_comments: Optional[str] = None  # Free text comments

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True  # Pydantic v2 renamed orm_mode

class UserFeedbackResponse(BaseModel):
    session_id: int
    user_id: int
    feedback_type: FeedbackTypeEnum
    positive_feedback: Optional[PositiveFeedbackEnum]
    negative_feedback: Optional[NegativeFeedbackEnum]
    additional_comments: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
