from sqlalchemy import select
from models.db_init import SessionLocal, Task
from time import sleep


def consume():
    db = SessionLocal()
    task = db.scalar(select(Task).where(Task.status == "pending"))
    if task is not None:
        print(f"Rozpoczęto zadanie nr {task.id}")
        task.status = "in_progress"
        db.commit()
        db.refresh(task)
        sleep(10)
        task.status = "done"
        db.commit()
        db.refresh(task)
        print(f"Skończono zadanie nr {task.id}")


while True:
    consume()
    sleep(3)
