from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_create_class():
    response = client.post("/classes", json={
        "name": "Test Yoga",
        "dateTime": "2025-06-15T10:00:00+05:30",
        "instructor": "Test Instructor",
        "availableSlots": 10
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Yoga"
    assert data["instructor"] == "Test Instructor"
    assert data["availableSlots"] == 10

def test_list_classes():
    response = client.get("/classes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_book_class():
    # Create a class first
    class_resp = client.post("/classes", json={
        "name": "Bookable Class",
        "dateTime": "2025-07-01T10:00:00+05:30",
        "instructor": "Booker",
        "availableSlots": 2
    })
    class_id = class_resp.json()["id"]
    # Book it
    book_resp = client.post("/book", json={
        "class_id": class_id,
        "client_name": "Test Client",
        "client_email": "test@example.com"
    })
    assert book_resp.status_code == 201
    data = book_resp.json()
    assert data["client_name"] == "Test Client"
    assert data["client_email"] == "test@example.com"

def test_get_bookings():
    email = "test2@example.com"
    # Create a class
    class_resp = client.post("/classes", json={
        "name": "Class for Booking",
        "dateTime": "2025-08-01T10:00:00+05:30",
        "instructor": "Booker",
        "availableSlots": 2
    })
    class_id = class_resp.json()["id"]
    # Book it
    client.post("/book", json={
        "class_id": class_id,
        "client_name": "Test Client 2",
        "client_email": email
    })
    # Get bookings
    resp = client.get(f"/bookings?email={email}")
    assert resp.status_code == 200
    bookings = resp.json()
    assert any(b["client_email"] == email for b in bookings) 