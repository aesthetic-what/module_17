from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine('sqlite:///taskmanager.db', echo=True)

session_local = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass