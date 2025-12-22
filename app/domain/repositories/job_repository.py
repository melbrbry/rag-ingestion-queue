from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.domain.models.job import Job, JobStatus
from app.domain.repositories.job_table import JobTable


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job: Job) -> None:
        record = JobTable(
            id=job.id,
            status=job.status.value,
            filename=job.filename,
            error_message=job.error_message,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        self.db.add(record)
        self.db.commit()

    def get(self, job_id: str) -> Optional[Job]:
        record = self.db.query(JobTable).filter(JobTable.id == job_id).first()
        if not record:
            return None

        return Job(
            id=record.id,
            status=JobStatus(record.status),
            filename=record.filename,
            error_message=record.error_message,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        error_message: Optional[str] = None
    ) -> None:
        record = self.db.query(JobTable).filter(JobTable.id == job_id).first()
        if not record:
            raise ValueError(f"Job {job_id} not found")

        record.status = status.value
        record.error_message = error_message
        record.updated_at = datetime.utcnow()

        self.db.commit()
