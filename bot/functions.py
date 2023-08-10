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


def delete_user(db: Session, user_id: int):
    user_to_delete = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        return True
    return False


def get_all_user_tasks(db: Session, user_id: int):
    user_tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()
    return user_tasks


def create_task(db: Session, name: str, user_id: int):
    new_task = models.Task(name=name, user_id=user_id)

    user_tasks_names = [task.name for task in get_all_user_tasks(db, user_id)]

    if name in user_tasks_names:
        return False

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def delete_task(db: Session, task_id: int):
    task_to_delete = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if task_to_delete:
        db.delete(task_to_delete)
        db.commit()
        return True
    return False


if __name__ == "__main__":
    # print(create_new_user(db, 1, 'test'))
    # print(delete_user(db, 182638302))
    # print(get_all_users(db))

    # print(create_task(db, "Task 2", 1))

    delete_task(db, 3)
    print([task.name for task in get_all_user_tasks(db, 1)])
