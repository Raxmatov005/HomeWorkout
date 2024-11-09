from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from passlib.hash import bcrypt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from models.model import *
from schemas import *
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText


SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"  # Make this a secure random string
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



##################################################    TOKEN    ################################################################




def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None




##################################################    PASSWORD    ################################################################



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)




##################################################    PASSWORD RESET   ################################################################



SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"  # Use a real secret key
RESET_TOKEN_EXPIRATION = 3600  # 1 hour

def generate_password_reset_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt="password-reset-salt")

def verify_password_reset_token(token: str) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=RESET_TOKEN_EXPIRATION)
    except Exception as e:
        return None
    return email


import smtplib
from email.mime.text import MIMEText

# Ensure your email credentials are securely stored and not hard-coded
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"

def send_reset_email(email: str, token: str):
    # Create the email message
    msg = MIMEText(f"Your password reset token is: {token}")
    msg["Subject"] = "Password Reset"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    # Connect to the SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Replace with your SMTP server and port
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())



##################################################    EMAIL MESSAGE   ################################################################




def send_reset_email(email: str, token: str):
    reset_link = f"http://yourapp.com/reset-password?token={token}"
    message = MIMEText(f"Click here to reset your password: {reset_link}")
    message["Subject"] = "Password Reset Request"
    message["From"] = "no-reply@yourapp.com"
    message["To"] = email
    
    with smtplib.SMTP("smtp.your-email-provider.com") as server:
        server.login("your-email-username", "your-email-password")
        server.sendmail("no-reply@yourapp.com", [email], message.as_string())




##################################################    HASHING PASSWORD   ################################################################



def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')



##################################################    USER    ################################################################



def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hash(user.password)
    
    # Convert gender enum to string, then lowercase
    new_user = user.gender.name.lower() if user.gender else None
    print(f"This is a gender of a user {new_user}")

    # Convert workout history enum to its value (string)
    workout_history = user.workout_history.value.lower() if user.workout_history else None
    print(workout_history)

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
        age=user.age,
        weight=user.weight,
        height=user.height,
        gender=new_user,  # Enum handled here
        goals=user.goals,
        workout_history=workout_history,  # Enum value (string) inserted
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





##################################################    WORKOUT CATEGORY    ################################################################



# Function to insert a workout category into the database
def create_category_in_db(db: Session, category: WorkoutCategoryCreate):
    db_category = WorkoutCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category



# Function to get a workout category by its name
def get_workout_category_by_name(db: Session, category_name: str):
    return db.query(WorkoutCategory).filter(WorkoutCategory.category_name == category_name).first()



# Function to update an existing workout category
def change_workout_category_in_db(db: Session, category_id: int, change_category: WorkoutCategoryChange):
    # Fetch the existing category from the database
    db_category = db.query(WorkoutCategory).filter(WorkoutCategory.id == category_id).first()

    # If the category doesn't exist, raise a 404 error
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # Update the category fields with the new data
    db_category.category_name = change_category.category_name
    db_category.description = change_category.description
    db_category.recommended_frequency = change_category.recommended_frequency

    # Commit the changes to the database
    db.commit()
    db.refresh(db_category)  # Refresh to return the updated category object

    return db_category



##################################################    PROGRAMM    ################################################################



def create_workout_program(db: Session, program: WorkoutProgramCreate, user_id: int):
    db_program = WorkoutProgram(
        frequency_per_week=program.frequency_per_week,
        total_duration=program.total_duration,
        progress=program.progress.value,  # Enum is automatically converted
        overall_goal=program.overall_goal.value,  # Enum is automatically converted
        workout_category_id=program.workout_category_id,
        start_date=program.start_date,
        end_date=program.end_date,
        user_id=user_id
    )
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

def change_workout_program_in_db(db: Session, program_id: int, change_program: WorkoutProgramChange):
    db_program = db.query(WorkoutProgram).filter(WorkoutProgram.id == program_id).first()

    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")

    db_program.frequency_per_week = change_program.frequency_per_week
    db_program.total_duration = change_program.total_duration
    db_program.progress = change_program.progress.value  # Enum handled here
    db_program.overall_goal = change_program.overall_goal.value  # Enum handled here
    db_program.active = change_program.active
    db_program.start_date = change_program.start_date
    db_program.end_date = change_program.end_date

    db.commit()
    db.refresh(db_program)

    return db_program


def get_workout_programs_by_user(db: Session, user_id: int):
    return db.query(WorkoutProgram).filter(WorkoutProgram.user_id == user_id).all()

def delete_program_in_db(db: Session, program_id: int):
    db_program = db.query(WorkoutProgram).filter(WorkoutProgram.id == program_id).first()
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found") 
    db.delete(db_program)
    db.commit()
    return {"message": "Program deleted successfully"}
    







##################################################    WORKOUT SESSION    ################################################################



# Workout Session CRUD
def create_workout_session(db: Session, session: WorkoutSessionCreate):
    # Verify that the program_id exists in the database
    program = db.query(WorkoutProgram).filter(WorkoutProgram.id == session.program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="WorkoutProgram with the specified ID does not exist.")
    
    db_session = WorkoutSession(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_sessions_by_program(db: Session, program_id: int):
    return db.query(WorkoutSession).filter(WorkoutSession.program_id == program_id).all()



# Function to update an existing workout session
def change_workout_session_in_db(db: Session, session_id: int, change_session: WorkoutSessionChange):
    db_session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()

    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_session.completion_status = change_session.completion_status
    db_session.user_feedback = change_session.user_feedback
    db_session.performance_notes = change_session.performance_notes
    db_session.calories_burned = change_session.calories_burned
    db_session.actual_date = change_session.actual_date
    db_session.scheduled_date = change_session.scheduled_date

    
    db.commit()
    db.refresh(db_session)  

    return db_session



def delete_session_in_db(db: Session, session_id: int):
    db_session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found") 
    db.delete(db_session)
    db.commit()
    return {"message": "Session deleted successfully"}




##################################################    WORKOUT EXERCISE    ################################################################


def create_exercise_in_db(db: Session, exercise: ExerciseCreate):
    db_exercise = Exercise(
        session_id=exercise.session_id,
        name=exercise.name,
        description=exercise.description,
        difficulty_level=exercise.difficulty_level.value,  # Enum handled here
        duration=exercise.duration,
        calories_burned=exercise.calories_burned,
        category_id=exercise.category_id,
        video_url=exercise.video_url,
        target_muscle=exercise.target_muscle.value  # Enum handled here
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def change_workout_exercise_in_db(db: Session, exercise_id: int, change_exercise: WorkoutExerciseChange):
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()

    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db_exercise.name = change_exercise.name
    db_exercise.description = change_exercise.description
    db_exercise.difficulty_level = change_exercise.difficulty_level.value  # Enum handled here
    db_exercise.duration = change_exercise.duration
    db_exercise.calories_burned = change_exercise.calories_burned
    db_exercise.video_url = change_exercise.video_url
    db_exercise.target_muscle = change_exercise.target_muscle.value  # Enum handled here

    db.commit()
    db.refresh(db_exercise)

    return db_exercise



def get_exercises_by_session(db: Session, session_id: int):
    return db.query(Exercise).filter(Exercise.session_id == session_id).all()

def delete_exercise_in_db(db: Session, exercise_id: int):
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found") 
    db.delete(db_exercise)
    db.commit()
    return {"message": "Exercise deleted successfully"}


##################################################    FEEDBACK    ################################################################


def create_user_feedback(db: Session, feedback: UserFeedbackCreate):
    db_feedback = UserFeedback(
        session_id=feedback.session_id,
        user_id=feedback.user_id,
        feedback_type=feedback.feedback_type.value,
        positive_feedback=feedback.positive_feedback.value if feedback.feedback_type == FeedbackTypeEnum.positive else None,
        negative_feedback=feedback.negative_feedback.value if feedback.feedback_type == FeedbackTypeEnum.negative else None,
        additional_comments=feedback.additional_comments
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def get_feedback_by_session_in_db(db: Session, session_id: int):
    return db.query(UserFeedback).filter(UserFeedback.session_id == session_id).all()




def delete_feedback_in_db(db: Session, feedback_id: int):
    db_feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found") 
    db.delete(db_feedback)
    db.commit()
    return {"message": "Feedback deleted successfully"}