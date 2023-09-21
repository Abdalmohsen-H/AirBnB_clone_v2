#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from models import storage
from sqlalchemy import Column, Integer, String, DateTime
from os import getenv
from sqlalchemy.ext.declarative import declarative_base

time_frmt = "%Y-%m-%dT%H:%M:%S.%f"

if getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()

else:  # if it is  afilestorage not db
    # in python3 whether you explicitly write class MyClass(object) or
    # just class MyClass, it's will be the same. as All classes
    # automatically inherit from the object class by default
    # so I am using this because other model will inherit base
    # and I want them to inherit object instead of declarative_base()
    Base = object


class BaseModel:
    """This is base class for all hbnb models
    it could handle both orm dbstorage or filestorage"""

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        id = Column(String(60), primary_key=true, nullable=False)
        created_at = column(DateTime, default=datetime.utcnow,
                            nullable=False)
        updated_at = column(DateTime, default=datetime.utcnow,
                            nullable=False)

    def __init__(self, *args, **kwargs):
        """instance intialization function to
        create a new model"""

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        storage.new(self) 
        for key, val in kwargs.items():
            if key == '__class__':
                continue
            setattr(self, key, val)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at,
                        time_frmt)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at,
                        time_frmt)

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(self.__class__.__name__, 
                                     self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()

        # remove _sa_instance_state key only if exist
        my_dict.pop('_sa_instance_state', None)

        return (my_dict)

    def delete(self):
        """ delete current instance from the storage (models.storage)
        by calling the method delete from FileStorage class
        we are using __init__ , So storage = FileStorage()"""
        storage.delete()
