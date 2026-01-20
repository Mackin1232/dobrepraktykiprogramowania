from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from asyncio import to_thread
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import pika
import json
import uuid
import time
from datetime import datetime
from typing import Optional

DATABASE_URL = "sqlite:///./jobs.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(String, primary_key=True, index=True) 
    people_count = Column(Integer, default=-1)        
    task_status = Column(String, default="PENDING")  
    analyzed_filename = Column(String, nullable=True) 
    
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)

RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'image_analysis_queue'

app = FastAPI(title="Image Analysis Producer API (DB-based)")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def publish_task(task_id: str, image_url: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        message_body = {"id": task_id, "url": image_url}
        
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message_body),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
        )
        connection.close()
        print(f"Zadanie {task_id} opublikowane.")
        
    except pika.exceptions.AMQPConnectionError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                            detail=f"Błąd połączenia z RabbitMQ: {e}")

def create_task_in_db(task_id: str, image_url: str):
    db = next(get_db())
    new_task = AnalysisResult(
        id=task_id, 
        image_url=image_url, 
        task_status="PENDING",
        people_count=-1,
        analyzed_filename=None
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

class AnalysisRequest(BaseModel):
    url: str

@app.post("/analyze_img")
async def analyze_image(request: AnalysisRequest):
    task_id = str(uuid.uuid4())
    try:
        create_task_in_db(task_id, request.url)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Błąd zapisu do bazy danych: {e}")
        
    await to_thread(publish_task, task_id, request.url)
    
    return {"message": "Image analysis task accepted", "id": task_id, "status": "PENDING"}

@app.get("/check_result/{task_id}")
def check_status(task_id: str):
    db = next(get_db())
    result = db.query(AnalysisResult).filter(AnalysisResult.id == task_id).first()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Zadanie o ID {task_id} nie istnieje.")
        
    if result.task_status != "COMPLETED" and result.task_status != "ERROR":
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail=f"Analiza dla ID {task_id} jest w toku. Status: {result.task_status}."
        )

    if result.task_status == "ERROR":
         raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail=f"Analiza zakończona błędem. Sprawdź logi Konsumenta.",
             headers={"X-Analyzed-Filename": result.analyzed_filename or "N/A"}
         )
        
    return {
        "id": result.id,
        "people_count": result.people_count,
        "status": result.task_status,
        "analyzed_filename": result.analyzed_filename
    }