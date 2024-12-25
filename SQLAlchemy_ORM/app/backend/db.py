from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy_utils import database_exists, create_database


engine = create_engine("sqlite:///parts_ordering.db", echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f'Database is created: {database_exists(engine.url)}')
        Base.metadata.create_all(engine)
