from dotenv import load_dotenv
import logging
import os

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
# from sshtunnel import SSHTunnelForwarder


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)




def create_engine_mysql():
    load_dotenv()
    username = os.environ.get("DB_username_local")
    password = os.environ.get("DB_password_local")
    db_name = os.environ.get("DB_name")
    engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost:3306")

    with engine.begin() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name};"))
    engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost:3306/{db_name}")
    return engine

def create_engine_db_rds():
    load_dotenv()
    username = os.environ.get("DB_username_local")
    password = os.environ.get("DB_password_local")
    host = os.environ.get("DB_host_local")
    port = os.environ.get("DB_port_local")
    db_name = os.environ.get("DB_name")
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{str(port)}")

    with engine.begin() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name};"))
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}")
    return engine


def create_session(engine):
    Session = sessionmaker(engine)
    session = Session()
    metadata = MetaData()
    return session, metadata
