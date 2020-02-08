from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from repost import config

url = make_url(config.database_url)
connect_args = {}

# SQLite driver only allows one thread by default to prevent multiple
# connections, but internally we are opening multiple connections so
# multiple threads can be used
if url.drivername == 'sqlite':
    connect_args['check_same_thread'] = False

engine = create_engine(url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
