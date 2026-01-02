from fastapi import APIRouter, UploadFile, Depends
import uuid
from datetime import datetime

from app.domain.models.job import Job, JobStatus
from app.services.dependencies import *
from app.domain.repositories.job_repository import JobRepository
from app.storage.file_storage import save_file
from app.domain.queue.base import QueueMessage
from app.domain.queue.base import QueueClient
from typing import Annotated

ingest_router = APIRouter()


@ingest_router.post("/ingest")
async def ingest_file(
    file: UploadFile,
    repo: Annotated[JobRepository, Depends(get_job_repository)],
    queue_client: Annotated[QueueClient, Depends(get_queue_client)],
    config: Annotated[dict, Depends(get_config)]
):
    # 1. Generate job ID
    job_id = str(uuid.uuid4())

    # 2. Upload file to S3
    bucket_name = config["s3"]["bucket_name"]
    object_key = save_file(file, job_id, bucket_name)

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
    
    # 4. Enqueue job for processing
    queue_client.send(QueueMessage(
        job_id=job.id,
        object_key=object_key,
        bucket_name=bucket_name
    ))

    # 5. Return job_id immediately
    return {"job_id": job_id}
