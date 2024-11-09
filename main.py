from fastapi import FastAPI
from database import engine, Base
from routers import user, program, session, exercise, feedback, workout
from authentication import reset_password, registration

# Create the FastAPI app
app = FastAPI()

# Create the database tables (this is optional if using migrations)
Base.metadata.create_all(bind=engine)

# Include the routers (modules that contain API routes)
app.include_router(registration.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(workout.router, prefix="/workout", tags=["Workout"])
app.include_router(program.router, prefix="/programs", tags=["Programs"])
app.include_router(session.router, prefix="/sessions", tags=["Sessions"])
app.include_router(exercise.router, prefix="/exercises", tags=["Exercises"])
app.include_router(feedback.router, prefix="/feedbacks", tags=["Feedback"])
# app.include_router(reset_password.router, prefix="/reset-password", tags=["Reset Password"])


# Root endpoint for testing if the API is up
@app.get("/")
async def root():
    return {"message": "Mobile Home-Workout App API is running"}
