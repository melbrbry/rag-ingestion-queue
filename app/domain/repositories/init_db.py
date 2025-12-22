from app.domain.repositories.database import engine, Base
from app.domain.repositories.job_table import JobTable

def init_db():
    Base.metadata.create_all(bind=engine)
