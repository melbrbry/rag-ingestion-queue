from fastapi import APIRouter, UploadFile, Depends, BackgroundTasks
import uuid
from datetime import datetime

from app.domain.models.job import Job, JobStatus
from app.api.dependencies import *
from app.domain.repositories.job_repository import JobRepository
from app.storage.file_storage import save_file
from app.workers.background import process_file

ingest_router = APIRouter()


@ingest_router.post("/ingest")
async def ingest_file(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    repo: JobRepository = Depends(get_job_repository),
):
    # 1. Generate job ID
    job_id = str(uuid.uuid4())

    # 2. Save file
    file_path = save_file(file, job_id)

    # 3. Create job record
    job = Job(
        id=job_id,
        status=JobStatus.PENDING,
        filename=file.filename,
        error_message=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    repo.create(job)

    # 4. Enqueue background ingestion
    background_tasks.add_task(process_file, job_id, file_path)

    # 5. Return job_id immediately
    return {"job_id": job_id}
