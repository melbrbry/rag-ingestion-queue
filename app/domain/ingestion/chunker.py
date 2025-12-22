from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import yaml
from dotenv import load_dotenv
from loguru import logger
import os

# Load environment variables from .env file
load_dotenv()

# Load configuration
with open("config.yml", "r") as config_file:
    config = yaml.safe_load(os.path.expandvars(config_file.read()))

chunking_config = config["chunking"]

def chunk_text(text: str) -> List[Document]:
    """
    Split text into chunks for embeddings.
    """

    logger.info(f"Chunking text with chunk size {chunking_config['chunk_size']} and overlap {chunking_config['overlap']}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunking_config["chunk_size"],
        chunk_overlap=chunking_config["overlap"],
    )

    chunks = text_splitter.create_documents([text])

    return chunks