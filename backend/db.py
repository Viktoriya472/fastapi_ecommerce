import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()


engine = create_engine(os.getenv('psql'), echo=True)
SessoinLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
