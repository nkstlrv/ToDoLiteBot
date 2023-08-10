from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()


def get_all_users(db: Session):
    all_users = db.query(models.User).all()
    return all_users


if __name__ == "__main__":
    print(get_all_users(db))
