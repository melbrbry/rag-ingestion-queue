import tempfile
from pathlib import Path
from PyPDF2 import PdfReader
from loguru import logger

from app.storage.file_storage import download_file


def parse_document(object_key: str, bucket_name: str) -> str:
    """
    Download file from S3, detect file type and extract text content.
    Returns full text as a string.
    """
    # Get file extension from object key
    ext = Path(object_key).suffix.lower()
    logger.info(f"Parsing document: s3://{bucket_name}/{object_key} with extension: {ext}")

    # Download file to a temporary location
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
        local_path = tmp_file.name

    download_file(object_key, bucket_name, local_path)

    try:
        if ext == ".txt":
            return Path(local_path).read_text(encoding="utf-8")

        elif ext == ".pdf":
            text = ""
            reader = PdfReader(local_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text

        else:
            raise ValueError(f"Unsupported file type: {ext}")
    finally:
        # Clean up temporary file
        Path(local_path).unlink(missing_ok=True)
