from app.domain.repositories.database import SessionLocal
from app.domain.repositories.job_repository import JobRepository
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_job_repository(db=Depends(get_db)):
    return JobRepository(db)