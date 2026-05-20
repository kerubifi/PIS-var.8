from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.adapter.out.listing_orm import Base


DATABASE_URL = "postgresql://user:password@localhost:5432/listing_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
