# Fitness Studio Booking API

A simple FastAPI backend for managing fitness class schedules and bookings.

## Features
- Create and list fitness classes
- Book a spot in a class
- View bookings by email
- Handles timezones (IST to UTC, and display in any timezone)
- Input validation and error handling
- Basic logging for key actions and errors

## Tech Stack
- Python
- FastAPI
- SQLite (via SQLAlchemy)
- Uvicorn (ASGI server)

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd Booking
   ```
2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Mac/Linux
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the API server**
   ```sh
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Create a Class
```sh
curl -X POST "http://localhost:8000/classes" -H "Content-Type: application/json" -d '{
  "name": "Yoga Flow",
  "dateTime": "2025-06-15T10:00:00+05:30",
  "instructor": "John Doe",
  "availableSlots": 20
}'
```

### List All Classes
```sh
curl http://localhost:8000/classes
```

### List Classes in Any Timezone
```sh
curl "http://localhost:8000/classes_in_timezone?tz=Asia/Kolkata"
```
- Replace `Asia/Kolkata` with any valid timezone (e.g., `UTC`, `US/Eastern`).
- Returns all classes with their times converted to the requested timezone.

### Book a Class
```sh
curl -X POST "http://localhost:8000/book" -H "Content-Type: application/json" -d '{
  "class_id": 1,
  "client_name": "Alice",
  "client_email": "alice@example.com"
}'
```

### View Bookings by Email
```sh
curl "http://localhost:8000/bookings?email=alice@example.com"
```

## Timezone Handling
- All class times are stored in UTC.
- When creating a class, submit the time in IST (or any timezone) using ISO 8601 format (e.g., `2025-06-15T10:00:00+05:30`).
- Use `/classes_in_timezone` to view class times in any timezone.

## Logging
- The app logs key actions (class creation, booking) and warnings (overbooking, missing class) to the console.
- Logging is set to INFO level by default.

## Notes
- Handles overbooking and input validation errors gracefully.
- Includes basic unit tests in `app/test_main.py`.

## Project Utilities

- **Seed file (`seed.py`)**: This script is provided to quickly populate your database with some example or demo data. You can run it manually (e.g., `python Booking/app/seed.py`) whenever you want to add sample classes and bookings for development or demonstration purposes.

- **Test file (`test_main.py`)**: This file contains automated tests for the API endpoints. You can run these tests using pytest (e.g., `pytest Booking/app/test_main.py`) to make sure your API behaves as expected and handles errors properly.


