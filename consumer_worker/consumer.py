# consumer_worker.py - Użycie SQLAlchemy do aktualizacji wyników

import numpy as np
import cv2
import requests
import pika
import json
import os
import time 
from typing import Dict, Any, Tuple, Optional
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Importowanie modelu z producer_api (lub jego kopi)
# W prawdziwej aplikacji model byłby w osobnym module shared_models.py
from producer import AnalysisResult, DATABASE_URL 
# Założenie: producer_api musi być w ścieżce dla tego importu

# --- Konfiguracja Bazy Danych dla Konsumenta ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Konfiguracja Workera ---
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'image_analysis_queue'
ANALYZED_IMAGES_FOLDER = 'analyzed_images' 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# --- Funkcje Bazy Danych ---

def update_task_status(task_id: str, status: str, people_count: int = -1, filename: Optional[str] = None):
    """Aktualizuje status zadania w DB."""
    db = SessionLocal()
    try:
        task = db.query(AnalysisResult).filter(AnalysisResult.id == task_id).first()
        if task:
            task.task_status = status
            task.people_count = people_count
            
            if filename:
                task.analyzed_filename = filename
                
            if status in ["COMPLETED", "ERROR"]:
                task.completed_at = datetime.utcnow()
                
            db.commit()
        else:
            print(f"Ostrzeżenie: Nie znaleziono zadania {task_id} w DB.")
    finally:
        db.close()

# --- Logika Biznesowa (bez zmian) ---

def get_file_extension_from_url(url: str) -> str:
    path = urlparse(url).path
    ext_part = path.split('.')[-1].lower()
    if len(ext_part) <= 4 and ext_part.isalnum():
        return ext_part
    return 'jpg'

def nr_ppl_and_get_content(url: str) -> Tuple[int, bytes, str]:
    # ... (Kod funkcji nr_ppl_and_get_content pozostaje bez zmian)
    image_content = b''
    try:
        img_response = requests.get(url, timeout=10, headers=HEADERS)
        img_response.raise_for_status() 
        
        image_content = img_response.content 
        file_extension = get_file_extension_from_url(url)
        
        img = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_COLOR)
        
        if img is None:
            return 0, image_content, file_extension 
            
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        frame = cv2.resize(img, (640, 480))
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))
        
        return len(boxes), image_content, file_extension

    except requests.exceptions.HTTPError as e:
        print(f"❌ Błąd HTTP {e.response.status_code} dla URL: {url}. Powód: {e}")
        return -1, image_content, '' 
    except Exception as e:
        print(f"❌ Nieznany błąd w analizie obrazu: {e}")
        return -1, image_content, '' 

# --- Logika Konsumenta ---

def callback(ch, method, properties, body):
    """Funkcja wywoływana po otrzymaniu wiadomości z kolejki."""
    task_id = "UNKNOWN"
    try:
        task: Dict[str, Any] = json.loads(body)
        task_id: str = task.get('id')
        image_url: str = task.get('url')
        
        print(f"\n▶️ Otrzymano zadanie {task_id}. Ustawiam status na PROCESSING.")
        update_task_status(task_id, "PROCESSING") # 1. Status na PROCESSING

        # 2. Analiza obrazu
        people_count, image_content, file_extension = nr_ppl_and_get_content(image_url)

        final_status = "COMPLETED"
        final_filename = None
        
        if people_count >= 0 and image_content:
            os.makedirs(ANALYZED_IMAGES_FOLDER, exist_ok=True)
            
            # Nazwa pliku: {id}_{liczba osób}.{rozszerzenie}
            final_filename = f"{task_id}_{people_count}.{file_extension}"
            image_filepath = os.path.join(ANALYZED_IMAGES_FOLDER, final_filename)

            with open(image_filepath, 'wb') as f:
                f.write(image_content)
            
            print(f"💾 Zapisano obraz: {image_filepath}")
        else:
            final_status = "ERROR"
            print("❌ Analiza zakończona błędem.")

        # 3. Aktualizacja bazy danych końcowym wynikiem i statusem
        update_task_status(task_id, final_status, people_count, final_filename)
        
        print(f"✅ Zakończono zadanie {task_id}. Status: {final_status}.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"❌ Krytyczny błąd podczas przetwarzania zadania {task_id}: {e}")
        # Aktualizacja statusu w DB w przypadku krytycznego błędu (np. błąd JSON)
        update_task_status(task_id, "ERROR")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_consumer():
    # ... (Kod funkcji start_consumer pozostaje bez zmian)
    print('🤖 Konsument startuje. Czekam na wiadomości...')
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=RABBITMQ_QUEUE,
            on_message_callback=callback
        )

        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"❌ Nie udało się połączyć z RabbitMQ. Błąd: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie przez użytkownika.")


if __name__ == '__main__':
    start_consumer()