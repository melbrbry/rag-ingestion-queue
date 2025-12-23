from fastapi import FastAPI
from app.services.api.routes.ingest import ingest_router
from app.services.api.routes.jobs import jobs_router
from app.domain.repositories.init_db import init_db

app = FastAPI()

# Initialize database tables
init_db()

# Register API router
app.include_router(ingest_router)
app.include_router(jobs_router)