from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Replace with your actual MySQL credentials
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASS = os.getenv("MYSQL_PASS", "1234")
MYSQL_DB   = os.getenv("MYSQL_DB", "combatdb")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class VideoEvent(Base):
    __tablename__ = "video_events"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    frame = Column(Integer)
    position = Column(String)
    timestamp = Column(String)

# Create tables if not exist
Base.metadata.create_all(bind=engine)