from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()


def get_all_users(db: Session):
    all_users = db.query(models.User).all()
    return [user.user_id for user in all_users]


def create_new_user(db: Session, user_id: int, username: str):
    new_user = models.User(user_id=user_id, username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


if __name__ == "__main__":
    # print(create_new_user(db, 2, 'test2'))
    print(get_all_users(db))
