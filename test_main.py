
from fastapi.testclient import TestClient
from main import app

# Create a test client for our FastAPI application
client = TestClient(app)


# Test the welcome endpoint
def test_home():
    response = client.get("/")

    # Check HTTP status
    assert response.status_code == 200

    # Check response data
    assert response.json() == {
        "message": "TaskFlow API is running"
    }


# Test retrieving all tasks
def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test creating a task
def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Pytest",
            "completed": False
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Learn Pytest"
