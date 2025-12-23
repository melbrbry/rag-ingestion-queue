import time
from app.services.worker.processor import process_job
from app.services.dependencies import *

def run():

    queue = get_queue_client(get_config())
    
    print("Worker started, waiting for messages...")

    while True:
        messages = queue.receive(max_messages=1)

        for message in messages:
            try:
                process_job(message["body"])
                queue.delete(message)

            except Exception as e:
                print(f"Error processing message: {e}")
                # message NOT deleted → retried by queue

        time.sleep(1)


if __name__ == "__main__":
    run()
