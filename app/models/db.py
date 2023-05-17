from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.common.connections import get_cloudsql_connection

engine = create_engine(
    "postgresql+pg8000://",
    creator=get_cloudsql_connection(),
)

Session = sessionmaker(bind=engine)
db = declarative_base()
session = Session()
