from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import pytz
import logging

from . import models, schemas, database

app = FastAPI(title="Fitness Studio Booking API")

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    """
    Dependency to get a SQLAlchemy session.
    Closes the session after use.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    """
    Initialize the database tables on app startup.
    """
    database.init_db()

@app.post("/classes", response_model=schemas.FitnessClassOut, status_code=status.HTTP_201_CREATED)
def create_class(fitness_class: schemas.FitnessClassCreate, db: Session = Depends(get_db)):
    """
    Create a new fitness class.
    Accepts class details in IST (or any timezone), converts to UTC for storage.
    Returns the created class.
    """
    # Convert IST to UTC
    ist = pytz.timezone("Asia/Kolkata")
    utc = pytz.utc
    dt_ist = fitness_class.dateTime
    if dt_ist.tzinfo is None:
        dt_ist = ist.localize(dt_ist)
    dt_utc = dt_ist.astimezone(utc)
    db_class = models.FitnessClass(
        name=fitness_class.name,
        date_time=dt_utc,
        instructor=fitness_class.instructor,
        available_slots=fitness_class.availableSlots
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    logger.info(f"Created class: {db_class.name} at {db_class.date_time} by {db_class.instructor}")
    return schemas.FitnessClassOut(
        id=db_class.id,
        name=db_class.name,
        dateTime=db_class.date_time,
        instructor=db_class.instructor,
        availableSlots=db_class.available_slots
    )

@app.get("/classes", response_model=List[schemas.FitnessClassOut])
def list_classes(db: Session = Depends(get_db)):
    """
    List all fitness classes (past and future).
    Returns all classes ordered by date and time.
    """
    classes = db.query(models.FitnessClass).order_by(models.FitnessClass.date_time).all()
    return [
        schemas.FitnessClassOut(
            id=c.id,
            name=c.name,
            dateTime=c.date_time,
            instructor=c.instructor,
            availableSlots=c.available_slots
        ) for c in classes
    ]

@app.get("/classes_in_timezone", response_model=List[schemas.FitnessClassOut])
def list_classes_in_timezone(tz: str = Query("Asia/Kolkata", description="Timezone, e.g., Asia/Kolkata, UTC, US/Eastern"), db: Session = Depends(get_db)):
    """
    List all fitness classes with their times converted to the requested timezone.
    Returns all classes ordered by date and time in the specified timezone.
    """
    try:
        target_tz = pytz.timezone(tz)
    except pytz.UnknownTimeZoneError:
        logger.warning(f"Unknown timezone requested: {tz}")
        raise HTTPException(status_code=400, detail=f"Unknown timezone: {tz}")
    classes = db.query(models.FitnessClass).order_by(models.FitnessClass.date_time).all()
    result = []
    for c in classes:
        # Assume c.date_time is stored in UTC
        dt_utc = c.date_time.replace(tzinfo=pytz.utc) if c.date_time.tzinfo is None else c.date_time.astimezone(pytz.utc)
        dt_local = dt_utc.astimezone(target_tz)
        result.append(schemas.FitnessClassOut(
            id=c.id,
            name=c.name,
            dateTime=dt_local,
            instructor=c.instructor,
            availableSlots=c.available_slots
        ))
    return result

@app.post("/book", response_model=schemas.BookingOut, status_code=status.HTTP_201_CREATED)
def book_class(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """
    Book a spot in a fitness class.
    Decreases available slots and creates a booking record.
    Handles overbooking and missing class errors.
    """
    db_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking.class_id).first()
    if not db_class:
        logger.warning(f"Booking failed: Class id {booking.class_id} not found.")
        raise HTTPException(status_code=404, detail="Class not found")
    if db_class.available_slots <= 0:
        logger.warning(f"Booking failed: No slots available for class id {booking.class_id}.")
        raise HTTPException(status_code=400, detail="No slots available")
    db_class.available_slots -= 1
    db_booking = models.Booking(
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    logger.info(f"Booked class id {booking.class_id} for {booking.client_name} ({booking.client_email})")
    return db_booking

@app.get("/bookings", response_model=List[schemas.BookingOut])
def get_bookings(email: str = Query(..., description="Client email address"), db: Session = Depends(get_db)):
    """
    Get all bookings for a given client email address.
    Returns a list of bookings for the specified email.
    """
    bookings = db.query(models.Booking).filter(models.Booking.client_email == email).all()
    return bookings 