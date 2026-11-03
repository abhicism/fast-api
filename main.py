from fastapi import FastAPI

from database.database import Base, engine
from models import TaskDB  # noqa: F401 - registers the model with Base.metadata
from routers.tasks import router as tasks_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")
app.include_router(tasks_router)


@app.get("/")
def home():
    return {"message": "TaskFlow API is running"}
