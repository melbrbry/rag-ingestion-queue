from pathlib import Path
from PyPDF2 import PdfReader
from loguru import logger

def parse_document(file_path: str) -> str:
    """
    Detect file type and extract text content.
    Returns full text as a string.
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    logger.info(f"Parsing document: {file_path} with extension: {ext}")

    if ext == ".txt":
        return path.read_text(encoding="utf-8")

    elif ext == ".pdf":
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    else:
        raise ValueError(f"Unsupported file type: {ext}")
