from app.db.session import SessionLocal
from app.initial_data import init_db


def seed():
    db = SessionLocal()
    init_db(db)
    db.close()

if __name__ == '__main__':
    seed()