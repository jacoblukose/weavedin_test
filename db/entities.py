from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column,DateTime, ForeignKey, Numeric, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class EntityConstructor(object):

    def __init__(self, engine):
        self.engine = engine

    def create(self):

        Base = declarative_base()
        metadata = MetaData()
        class Item(Base):
            
            print self.engine
            __tablename__ = "item"
            
            id = Column(Integer, primary_key = True)
            name = Column(String(20),nullable = False)
            brand = Column(String(20),nullable = False)
            category = Column(String(20),nullable = False)
            productCode = Column(String(15),nullable = False)
            
            user=Column(String(50),nullable = False)
            created_date = Column(DateTime(), default=datetime.now)
            updated_date  = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

            variants = relationship("Variant", back_populates="variants")

        class Variant(Base):
            
            __tablename__ = "variants"

            id = Column(Integer, primary_key = True)
            name = Column(String(50),nullable = False)
            sellingPrice = Column(Float,nullable = False)
            costPrice = Column(Float,nullable = False)
            quantity = Column(Integer, nullable = False)
            
            user=Column(String(50),nullable = False)
            created_date = Column(DateTime(), default=datetime.now)
            updated_date  = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
            
            item_id = Column(Integer,ForeignKey("item.id"))
            item = relationship("Item", back_populates="variants")
            
            properties = relationship("Property", uselist=False, back_populates="variant")


        class Property(Base):
           
            __tablename__ = "properties"
           
            id = Column(Integer, primary_key = True)
            cloth = Column(String(10),nullable = False)
            color = Column(String(10),nullable = False)
            size = Column(String(10),nullable = False)

            created_date = Column(DateTime(), default=datetime.now)
            updated_date = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

            variant_id = Column(Integer,ForeignKey("variants.id"))
            variant = relationship("Variant", back_populates="properties")


        Base.metadata.create_all(self.engine)
   