import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Set DB path to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'booking.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Print DB existence status
if os.path.exists(DB_PATH):
    print(f"Database found at: {DB_PATH}")
else:
    print(f"Database NOT found at: {DB_PATH}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def print_all_classes():
    """Print all entries in the fitness_classes table for debugging."""
    from .models import FitnessClass  # Correct model name
    session = SessionLocal()
    classes = session.query(FitnessClass).all()
    for c in classes:
        print(f"Class: id={c.id}, name={c.name}, date_time={c.date_time}, instructor={c.instructor}, available_slots={c.available_slots}")
    session.close() 