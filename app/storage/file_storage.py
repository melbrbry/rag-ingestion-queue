import os
from pathlib import Path
from fastapi import UploadFile

BASE_DIR = Path("./data/uploads")
BASE_DIR.mkdir(parents=True, exist_ok=True)

def save_file(file: UploadFile, job_id: str) -> str:
    """
    Save the uploaded file to disk.
    Returns the path.
    """
    filename = f"{job_id}_{file.filename}"
    file_path = BASE_DIR / filename

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return str(file_path)
