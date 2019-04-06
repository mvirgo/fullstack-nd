import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class CatalogItem(Base):
    __tablename__ = 'catalog_item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(500))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category) 

    # Function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'        : self.name,
           'description' : self.description,
           'id'          : self.id,
           'category'    : self.category,
       }


def main():
    engine = create_engine('sqlite:///itemcatalog.db') 
    Base.metadata.create_all(engine)
    return


if __name__ == "__main__":
    main()
