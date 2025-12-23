from app.domain.repositories.database import SessionLocal
from app.domain.repositories.job_repository import JobRepository
from fastapi import Depends
import os
import yaml
from dotenv import load_dotenv
from typing import Annotated
from app.infra.queue.factory import QueueFactory
from app.domain.queue.base import QueueClient

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_config():
    # Load environment variables from .env file
    load_dotenv()

    # Load configuration
    with open("config.yml", "r") as config_file:
        config = yaml.safe_load(os.path.expandvars(config_file.read()))

    return config


def get_job_repository(db=Depends(get_db)):
    return JobRepository(db)

def get_queue_client(config: Annotated[dict, Depends(get_config)]) -> QueueClient:
    queue_factory = QueueFactory()
    queue_backend = config["queue"]["backend"]
    queue_config = config["queue"][queue_backend]
    queue_client = queue_factory.get_queue(queue_backend, queue_config)
    return queue_client