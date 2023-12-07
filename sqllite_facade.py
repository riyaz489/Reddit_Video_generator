from typing import List

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# Define the SQLite database connection string
db_url = 'sqlite:///posts.db'

# Create a SQLAlchemy engine
engine = create_engine(db_url, echo=True)  # Set echo to True for debugging

# Declare a base class for declarative class definitions
Base = declarative_base()

# Define a sample model class
class Post(Base):
    __tablename__ = 'posts'
    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    author = Column(String(50))

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
# session = Session()


def add_post( post):

    with Session() as session:
        # Example: Adding a new user to the database
        #     session.execute(text('drop table user'))

        session.add(post)
        session.commit()
        session.close()


def bulk_add_post(details: List):
    with Session() as session:

        session.bulk_save_objects(details)
        session.commit()
        session.close()




def filter_post(ids):
    with Session() as session:
        all_users = session.query(Post).filter(Post.id.in_(ids)).all()

        t = [r for r in all_users]
        session.close()

        return t

def delete_post(ids):
    with Session() as session:
        session.query(Post).filter(Post.id.in_(ids)).delete()
        session.commit()
        session.close()





