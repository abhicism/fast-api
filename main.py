from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import Base, engine
from models import TaskDB  # noqa: F401 - registers the model with Base.metadata
from routers.tasks import router as tasks_router
app = FastAPI(title="TaskFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(tasks_router)


@app.get("/")
def home():
    return {"message": "TaskFlow API is running"}
