from datetime import datetime, timedelta
import pytz
from .database import SessionLocal, init_db
from .models import FitnessClass

def seed():
    init_db()
    db = SessionLocal()
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    classes = [
        FitnessClass(name="Yoga Flow", date_time=ist.localize(now + timedelta(days=1)), instructor="John Doe", available_slots=20),
        FitnessClass(name="Zumba", date_time=ist.localize(now + timedelta(days=2, hours=2)), instructor="Jane Smith", available_slots=15),
        FitnessClass(name="HIIT", date_time=ist.localize(now + timedelta(days=3, hours=1)), instructor="Mike Lee", available_slots=10),
    ]
    db.add_all(classes)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed() 