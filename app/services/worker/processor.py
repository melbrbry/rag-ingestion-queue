from app.domain.repositories.database import SessionLocal
from app.domain.repositories.job_repository import JobRepository
from app.domain.models.job import JobStatus
from app.domain.ingestion.parser import parse_document
from app.domain.ingestion.chunker import chunk_text
from app.domain.ingestion.vector_store import upsert_vectors

def process_job(message: dict):
    job_id = message["job_id"]
    object_key = message["object_key"]
    bucket_name = message["bucket_name"]

    db = SessionLocal()
    repo = JobRepository(db)

    job = repo.get(job_id)

    if not job:
        db.close()
        raise RuntimeError(f"Job {job_id} not found")

    # Idempotency guard
    if job.status == JobStatus.COMPLETED:
        db.close()
        return

    if job.status == JobStatus.PROCESSING:
        db.close()
        return

    try:

        repo.update_status(job_id, JobStatus.PROCESSING)

        # 1 Parse file from S3
        text = parse_document(object_key, bucket_name)

        # 2 Chunk text
        chunks = chunk_text(text)

        # 3 Upsert into vector DB
        upsert_vectors(job_id, chunks)

        # 4 Mark job completed
        repo.update_status(job_id, JobStatus.COMPLETED)


    except Exception as e:
        repo.update_status(job_id, JobStatus.FAILED, error_message=str(e))
        raise

    finally:
        db.close()
