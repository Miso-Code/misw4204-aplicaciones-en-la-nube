from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

db_uri = os.environ.get('DB_URI')

engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
db = declarative_base()
session = Session()
