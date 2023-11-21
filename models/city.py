#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    if storage_type == 'db':
        name = Column(String(123), nullable=False)
        state_id = Column(String(60), ForeignKey('state_id'), nullable=False)
        places = relationship('Place', backref='cities',
                                cascade='all, delete, delete-orphan')
    else:
        name = ''
        state_id = ''
