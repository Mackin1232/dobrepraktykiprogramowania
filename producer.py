from sqlalchemy import select
from models.db_init import Base, SessionLocal, engine, Task

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


for i in range(100):
    task = Task(status="pending")
    with SessionLocal() as session:
        session.add(task)
        session.commit()

with SessionLocal() as session:
    tasks = session.scalars(select(Task)).all()
    for task in tasks:
        print(task.to_dict())