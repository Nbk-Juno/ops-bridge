from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
assert DATABASE_URL is not None, "DATABASE_URL not set in .env"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
