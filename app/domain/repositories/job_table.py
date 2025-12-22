from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.domain.repositories.database import Base


class JobTable(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
