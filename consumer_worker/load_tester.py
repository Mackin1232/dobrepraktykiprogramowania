# load_tester.py

import requests
import json
import threading
import time
from typing import List

# --- Konfiguracja ---
API_URL = "http://127.0.0.1:8000/analyze_img"
NUM_REQUESTS = 50
TIMEOUT = 50  # Timeout dla żądania HTTP (musi być dłuższy niż RabbitMQ RPC TIMEOUT)
THREADS_PER_BATCH = 50 # Liczba wątków do uruchomienia jednocześnie
# Lista różnych obrazów do analizy (możesz ją rozszerzyć)
IMAGE_URLS: List[str] = [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlqUp32WpfXLaXtdHMr5qU49gcoXy9tFTu-Q&s", # 4 osoby
    "https://img.freepik.com/premium-photo/diverse-people-together-teamwork-partnership_53876-52114.jpg?semt=ais_hybrid&w=740&q=80", # 2 osoby
    "https://img.freepik.com/free-photo/people-posing-together-registration-day_23-2149096793.jpg?semt=ais_hybrid&w=740&q=80", # 1 osoba
    "https://media.gettyimages.com/id/200244581-003/photo/large-crowd-of-people-looking-up-smiling-portrait-elevated-view.jpg?s=612x612&w=gi&k=20&c=jBXSpcZ2KmsX9pBLlGurH3sM2qCvQ7stgT-EiA_E_VQ=", # 1 osoba
    "https://allprodad.com/wp-content/uploads/2021/03/05-12-21-happy-people.jpg", # Wiele osób
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXIRAvqxFE9DnKGYMNKLjvVC-XdY-EJopQkw&s", # 0 osób
]
# Powtarzamy listę URLi, aby mieć 200 unikalnych zadań
ALL_URLS = (IMAGE_URLS * (NUM_REQUESTS // len(IMAGE_URLS) + 1))[:NUM_REQUESTS]


# --- Logika Wysłania Żądania ---

def send_request(request_id: int, url: str, results: List):
    """Wysyła żądanie POST do API i zapisuje wynik."""
    start_time = time.time()
    result_data = {
        "id": request_id,
        "url": url,
        "status": "FAILED",
        "people_count": "N/A",
        "latency_ms": -1
    }

    try:
        payload = json.dumps({"url": url})
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(
            API_URL, 
            data=payload, 
            headers=headers, 
            timeout=TIMEOUT
        )
        
        latency = (time.time() - start_time) * 1000 # Czas w ms
        
        result_data["latency_ms"] = round(latency)

        if response.status_code == 200:
            people_count = response.json()
            result_data["status"] = "SUCCESS"
            result_data["people_count"] = people_count
            print(f"✅ Request {request_id} (URL: {url[:30]}...): SUCCESS, {people_count} osób. Latency: {latency:.2f}ms")
        else:
            result_data["status"] = f"HTTP {response.status_code}"
            result_data["people_count"] = response.text
            print(f"❌ Request {request_id} (URL: {url[:30]}...): ERROR, {response.status_code}. Latency: {latency:.2f}ms")
            
    except requests.exceptions.Timeout:
        result_data["status"] = f"TIMEOUT ({TIMEOUT}s)"
        print(f"❌ Request {request_id} (URL: {url[:30]}...): TIMEOUT.")
    except requests.exceptions.RequestException as e:
        result_data["status"] = f"REQUEST_ERROR: {e.__class__.__name__}"
        print(f"❌ Request {request_id} (URL: {url[:30]}...): REQUEST_ERROR.")
    finally:
        results.append(result_data)


# --- Główna Logika ---

def run_load_test():
    """Uruchamia test obciążeniowy z równoległym wysyłaniem żądań."""
    
    global_start_time = time.time()
    all_results = []
    
    print(f"Starting load test: {NUM_REQUESTS} requests, {THREADS_PER_BATCH} threads per batch.")

    threads: List[threading.Thread] = []
    
    for i in range(NUM_REQUESTS):
        thread_id = i + 1
        url = ALL_URLS[i]
        
        # Tworzenie wątku
        thread = threading.Thread(target=send_request, args=(thread_id, url, all_results))
        threads.append(thread)
        thread.start()
        
        # Ograniczanie liczby aktywnych wątków do THREADS_PER_BATCH
        if len(threads) >= THREADS_PER_BATCH:
            # Poczekaj na zakończenie pierwszej partii wątków
            for t in threads:
                t.join()
            threads = []

    # Czekaj na zakończenie ostatnich wątków
    for t in threads:
        t.join()

    global_end_time = time.time()
    total_duration = global_end_time - global_start_time

    # --- Statystyki ---
    
    successful_requests = [r for r in all_results if r['status'] == 'SUCCESS']
    failed_requests = [r for r in all_results if r['status'] != 'SUCCESS']
    
    latencies = [r['latency_ms'] for r in successful_requests]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0

    print("\n" + "="*50)
    print("               TEST COMPLETED")
    print("="*50)
    print(f"Total Requests Sent: {NUM_REQUESTS}")
    print(f"Total Time Taken: {total_duration:.2f} seconds")
    print(f"Successful Requests: {len(successful_requests)}")
    print(f"Failed Requests (Timeout/Error): {len(failed_requests)}")
    print(f"Average Latency (Success): {avg_latency:.2f} ms")
    print("="*50)

if __name__ == "__main__":
    run_load_test()