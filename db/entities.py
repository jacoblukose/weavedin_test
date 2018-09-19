from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column,DateTime, ForeignKey, Numeric, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
class EntityConstructor(object):

    def __init__(self, engine):
        self.engine = engine


    def create(self):
        metadata = MetaData()
        Base.metadata.create_all(self.engine)



class Item(Base):
        
        __tablename__ = "item"
        name = Column(String(20),nullable = False)
        brand = Column(String(20),nullable = False)
        category = Column(String(20),nullable = False)
        productCode = Column(String(15),
                       nullable = False, 
                       primary_key = True,
                       default="abcd")
        
        created_date = Column(DateTime(), default=datetime.now)
        updated_date  = Column(DateTime(), default=datetime.now, 
                               onupdate=datetime.now)

        variants = relationship("Variant", back_populates="item")

class Variant(Base):
        
        __tablename__ = "variants"

        # id = Column(Integer, primary_key = True)

        var_code = Column(String(100),
                  nullable = False,
                  primary_key = True,
                  default = "abcd_variant")

        name = Column(String(50),nullable = False)
        sellingPrice = Column(Float,nullable = False)
        costPrice = Column(Float,nullable = False)
        quantity = Column(Integer, nullable = False)
        
        created_date = Column(DateTime(), default=datetime.now)
        updated_date  = Column(DateTime(), default=datetime.now, 
                               onupdate=datetime.now)
        
        item_id = Column(String(15),ForeignKey("item.productCode"))
        item = relationship("Item", back_populates="variants")
        
        properties = relationship("Property", uselist=False, 
                               back_populates="variant")


class Property(Base):
       
        __tablename__ = "properties"
       
        id = Column(Integer, primary_key = True)

        cloth = Column(String(50),nullable = True)
        color = Column(String(50),nullable = True)
        size = Column(String(10),nullable = True)

        created_date = Column(DateTime(), default=datetime.now)
        updated_date = Column(DateTime(), default=datetime.now, 
                              onupdate=datetime.now)

        variant_code = Column(String(100),ForeignKey("variants.var_code"))

        variant = relationship("Variant", back_populates="properties")


class Changelog(Base):
        __tablename__ = "changelog"

        id = Column(Integer, primary_key = True)
        
        mode = Column(String(50),nullable = False)
        created_date = Column(DateTime(), default=datetime.now)

        user = Column(String(50),nullable = True)

        item_category = Column(Boolean, default=False)
        variants_category = Column(Boolean, default=False)
        properties_category = Column(Boolean, default=False)

        item_data = Column(String(500),nullable = True)
        variants_data = Column(String(500),nullable = True)
        properties_data = Column(String(500),nullable = True)













