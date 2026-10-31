# Import FastAPI to create our API application
# Depends is used for dependency injection
# HTTPException is used to return HTTP errors
from fastapi import FastAPI, Depends, HTTPException

# BaseModel validates incoming data
# ConfigDict configures Pydantic model behavior
from pydantic import BaseModel, ConfigDict

# Import SQL data types and SELECT query builder
from sqlalchemy import String, Boolean, Integer, select

# Session manages database operations
# Mapped and mapped_column define database table columns
from sqlalchemy.orm import Session, Mapped, mapped_column

# Import database configuration
# Base is the parent class for database models
# engine connects SQLAlchemy to PostgreSQL
# get_db provides and closes database sessions
from database import Base, engine, get_db


# Create the FastAPI application
app = FastAPI(title="TaskFlow API")


# ==========================================
# 1. SQLALCHEMY MODEL
# ==========================================

# This class defines the actual PostgreSQL table
class TaskDB(Base):

    # Name of the table in PostgreSQL
    __tablename__ = "tasks"

    # Define the ID column
    id: Mapped[int] = mapped_column(
        Integer,           # Database column type: Integer
        primary_key=True,  # Each task gets a unique primary key
        index=True         # Create an index for faster ID lookups
    )

    # Define the title column
    title: Mapped[str] = mapped_column(
        String(200)        # String column with maximum 200 characters
    )

    # Define the completed column
    completed: Mapped[bool] = mapped_column(
        Boolean,           # Database column type: Boolean
        default=False      # New tasks are incomplete by default
    )


# ==========================================
# 2. PYDANTIC MODEL - INPUT VALIDATION
# ==========================================

# This model validates data received from the client
class TaskCreate(BaseModel):

    # Task title is required and must be a string
    title: str

    # completed is optional
    # If the client doesn't provide it, default is False
    completed: bool = False


# ==========================================
# 3. PYDANTIC MODEL - API RESPONSE
# ==========================================

# This model defines the structure of API responses
class TaskResponse(BaseModel):

    # Allow Pydantic to read data directly from
    # SQLAlchemy objects using their attributes
    model_config = ConfigDict(from_attributes=True)

    # Fields returned to the client
    id: int
    title: str
    completed: bool


# ==========================================
# 4. CREATE DATABASE TABLE
# ==========================================

# Create all tables defined using Base
# If the tasks table already exists, it won't recreate it
Base.metadata.create_all(bind=engine)


# ==========================================
# 5. HOME ROUTE
# ==========================================

# GET endpoint to check whether the API is running
@app.get("/")
def home():

    # Return a simple JSON response
    return {"message": "TaskFlow API is running"}


# ==========================================
# 6. GET ALL TASKS
# ==========================================

# GET endpoint to retrieve all tasks
# response_model ensures every returned task follows TaskResponse
@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db)  # Get a database session from FastAPI
):

    # Build a SELECT query to retrieve all tasks
    result = db.scalars(select(TaskDB)).all()

    # Return all retrieved task records
    return result


# ==========================================
# 7. CREATE A NEW TASK
# ==========================================

# POST endpoint to create and save a new task
# status_code=201 means resource successfully created
@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,                   # Validate incoming JSON data
    db: Session = Depends(get_db)       # Get database session
):

    # Convert Pydantic model into a dictionary
    # ** unpacks dictionary keys as keyword arguments
    # Create a new SQLAlchemy database object
    new_task = TaskDB(**task.model_dump())

    # Add the new task to the database session
    # It is not permanently saved yet
    db.add(new_task)

    # Commit the transaction
    # This permanently saves the task to PostgreSQL
    db.commit()

    # Refresh the object with values from the database
    # For example, retrieve the automatically generated ID
    db.refresh(new_task)

    # Return the newly created task
    return new_task


# ==========================================
# 8. GET TASK BY ID
# ==========================================

# GET endpoint to retrieve one specific task
# task_id comes from the URL
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,                       # Receive task ID from URL
    db: Session = Depends(get_db)       # Get database session
):

    # Search for a task using its primary key
    # db.get() returns the task object or None
    task = db.get(TaskDB, task_id)

    # Check whether the requested task exists
    if task is None:

        # If not found, return HTTP 404 error
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Return the matching task
    return task