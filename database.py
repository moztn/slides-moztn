from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine("sqlite://" + config.DATABASE, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, 
      autoflush=False,bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  #We only need init_db to create the database and tables
  import models
  Base.metadata.create_all(bind=engine)
