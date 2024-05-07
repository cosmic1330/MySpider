from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql://root:secret@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()