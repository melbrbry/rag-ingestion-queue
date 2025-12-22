from app.domain.repositories.database import SessionLocal
from app.domain.repositories.job_repository import JobRepository
from app.domain.models.job import JobStatus
from app.domain.ingestion.parser import parse_document
from app.domain.ingestion.chunker import chunk_text
from app.domain.ingestion.vector_store import upsert_vectors

def process_file(job_id: str, file_path: str):
    db = SessionLocal()
    repo = JobRepository(db)

    try:
        repo.update_status(job_id, JobStatus.PROCESSING)

        # 1 Parse file
        text = parse_document(file_path)

        # 2 Chunk text
        chunks = chunk_text(text)

        # 3 Upsert into vector DB
        upsert_vectors(job_id, chunks)

        # 4 Mark job completed
        repo.update_status(job_id, JobStatus.COMPLETED)

    except Exception as e:
        repo.update_status(job_id, JobStatus.FAILED, error_message=str(e))