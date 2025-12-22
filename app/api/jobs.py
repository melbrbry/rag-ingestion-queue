from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import *
from app.domain.repositories.job_repository import JobRepository
from app.domain.models.job import JobStatus

jobs_router = APIRouter()


@jobs_router.get("/jobs/{job_id}")
def get_job_status(job_id: str, repo: JobRepository = Depends(get_job_repository)):
    job = repo.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "status": job.status.value,
        "filename": job.filename,
        "error_message": job.error_message,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
    }
