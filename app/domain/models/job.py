from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Job:
    id: str
    status: JobStatus
    filename: str
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
