#!/usr/bin/python3
# Configuration

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Class definitions


class Restaurant(Base):

    # Table information
    __tablename__ = 'restaurant'

    # Mappers
    name = Column(
        String(80), nullable=False
    )
    id = Column(
        Integer, primary_key=True
    )


class MenuItem(Base):

    # Table information
    __tablename__ = 'menu_item'

    # Mappers
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

# End of file
engine = create_engine(
    'sqlite:///restaurantmenu.db'
)
Base.metadata.create_all(engine)
