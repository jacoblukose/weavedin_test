from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import  MetaData
from sqlalchemy.ext.declarative import declarative_base


__all__ = ["DatabaseConnection", "DatabaseSession"]


class DatabaseConnection(object):

    def __init__(self, url):
        self.engine = create_engine(url, pool_recycle=3600)
        
    def __enter__(self):
        # make a database connection and return it
        self.conn = self.engine.connect()
        return self.conn, self.engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        self.conn.close()



class DatabaseSession(object):

    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.session = Session(self.engine)

        # NB: following line is not needed if instances of SQL entities are replaced with other classes,
        # before passing results to business logic and above layers (which is recommended!)
        # Here for simplicity, data access layer entities are passed above to business logic;
        self.session.expire_on_commit = False
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None