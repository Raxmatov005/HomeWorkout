from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from sqlalchemy import Enum
import enum

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

class JointEnum(enum.Enum):
    shoulder = "shoulder"
    elbow = "elbow"
    wrist = "wrist"
    hip = "hip"
    knee = "knee"
    ankle = "ankle"
    spine = "spine"
    neck = "neck"

class MuscleEnum(enum.Enum):
    shoulders = "shoulders"
    biceps = "biceps"
    triceps = "triceps"
    forearms = "forearms"
    chest = "chest"
    glutes = "glutes"
    quadriceps = "quadriceps"
    hamstrings = "hamstrings"
    calves = "calves"
    back = "back"
    core = "core"
    neck = "neck"

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

##################################################    USER    ################################################################

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    gender = Column(Enum(GenderEnum), nullable=False)  
    goals = Column(String)
    workout_history = Column(Enum(WorkoutHistoryEnum), nullable=True)  
    progress_status = Column(Integer, nullable=True)
    workout_frequency = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workout_programs = relationship("WorkoutProgram", back_populates="user")
    health_conditions = relationship("UserInjuries", back_populates="user")
    feedback = relationship("UserFeedback", back_populates="user")

##################################################    USER HEALTH    ################################################################

class Injuries(Base):
    __tablename__ = "injuries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    joint_affected = Column(Enum(JointEnum), nullable=True)  
    muscle_affected = Column(Enum(MuscleEnum), nullable=True)  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to UserInjuries
    user_conditions = relationship("UserInjuries", back_populates="injury")

class UserInjuries(Base):
    __tablename__ = "user_injuries"  # Updated to user_injuries

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    injuries_id = Column(Integer, ForeignKey('injuries.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="health_conditions")
    injury = relationship("Injuries", back_populates="user_conditions")

##################################################    WORKOUT CATEGORY    ################################################################

class WorkoutCategory(Base):
    __tablename__ = "workout_categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    description = Column(String)
    recommended_frequency = Column(Integer)

    # Relationship
    exercises = relationship("Exercise", back_populates="category")

##################################################    WORKOUT PROGRAM    ################################################################

class WorkoutProgram(Base):
    __tablename__ = "workout_programs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    frequency_per_week = Column(Integer)
    total_duration = Column(Integer)
    progress = Column(Enum(ProgressEnum), nullable=False)  
    overall_goal = Column(Enum(GoalEnum), nullable=False)  
    workout_category_id = Column(Integer, ForeignKey('workout_categories.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="workout_programs")
    sessions = relationship("WorkoutSession", back_populates="program")

##################################################    WORKOUT SESSION    ################################################################

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey('workout_programs.id'))
    completion_status = Column(Boolean, default=False)
    user_feedback = Column(String, nullable=True)
    performance_notes = Column(String, nullable=True)
    calories_burned = Column(Float, nullable=True)
    actual_date = Column(DateTime, nullable=True)
    scheduled_date = Column(DateTime)

    # Relationships
    program = relationship("WorkoutProgram", back_populates="sessions")
    exercises = relationship("Exercise", back_populates="session")  # Added missing exercises relationship
    feedback = relationship("UserFeedback", back_populates="session")

##################################################    WORKOUT EXERCISE    ################################################################

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('workout_sessions.id'))
    name = Column(String)
    description = Column(String)
    difficulty_level = Column(Enum(DifficultyEnum), nullable=False)  
    duration = Column(Integer)
    calories_burned = Column(Float)
    category_id = Column(Integer, ForeignKey('workout_categories.id'))
    video_url = Column(String)
    target_muscle = Column(Enum(TargetMuscleEnum), nullable=False)  

    # Relationships
    session = relationship("WorkoutSession", back_populates="exercises")  # Fixed back_populates to session
    category = relationship("WorkoutCategory", back_populates="exercises")

##################################################    USER FEEDBACK    ################################################################

class UserFeedback(Base):
    __tablename__ = 'userfeedback'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    feedback_type = Column(Enum(FeedbackTypeEnum), nullable=False)
    positive_feedback = Column(Enum(PositiveFeedbackEnum), nullable=True)  
    negative_feedback = Column(Enum(NegativeFeedbackEnum), nullable=True)  
    additional_comments = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="feedback")
    session = relationship("WorkoutSession", back_populates="feedback")
