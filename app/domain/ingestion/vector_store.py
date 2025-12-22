import os
import yaml
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_core.documents import Document
from loguru import logger
import time
from functools import wraps

# Load environment variables from .env file
load_dotenv()

# Load configuration
with open("config.yml", "r") as config_file:
    config = yaml.safe_load(os.path.expandvars(config_file.read()))

pinecone_config = config["pinecone"]

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_config["api_key"])

index = pc.Index(host= pinecone_config["host_name"])

def retry_with_backoff(retries=3, backoff_in_seconds=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        logger.error(f"Upsert to Pinecone failed after {retries} attempts: {e}")
                        raise
                    logger.warning(f"Transient failure while upserting to Pinecone: {e}. Retrying in {backoff_in_seconds ** attempt} seconds...")
                    time.sleep(backoff_in_seconds ** attempt)
        return wrapper
    return decorator

@retry_with_backoff(retries=3, backoff_in_seconds=2)
def upsert_vectors(job_id: str, chunks: list[Document]):
    """
    Upsert chunks to Pinecone.
    Each vector ID is prefixed by job_id for isolation.
    """
    vectors = [
        {
            "_id": f"{job_id}_{i}",
            "text": chunk.page_content,
        }
        for i, chunk in enumerate(chunks)
    ]

    logger.info(f"Upserting {len(vectors)} vectors for job {job_id} to Pinecone.")

    index.upsert_records("default-ns", vectors)

    logger.info(f"Successfully upserted vectors.")
