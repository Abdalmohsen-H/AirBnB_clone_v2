#!/usr/bin/python3
"""This module defines a class to manage DATABASE storage for hbnb clone"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os


class DBStorage:
    """This class manages storage of hbnb models in SQL format"""
    __engine = None
    __session = None

    def __init__(self):
        """
        Create the engine (self.__engine)
        """
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        database = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        self.__engine = create_engine(
                        'mysql+mysqldb://{}:{}@{}/{}'
                        .format(user, password, host, database),
                        pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

        if env != 'test':
            self.reload()

    def all(self, cls=None):
        """
        Query on the current database session (self.__session) all
        objects depending on the class name (argument cls)
        If cls=None,
        query all types of objects
        (User, State, City, Amenity, Place, and Review)
        This method must return a dictionary: (like FileStorage)
        key = <class-name>.<object-id>
        value = object
        """
        classes = [User, State, City, Amenity, Place, Review]
        results = {}

        if cls is not None:
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                results[key] = obj
        else:
            for clsname in classes:
                query = self.__session.query(clsname).all()
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    results[key] = obj

        return results

    def new(self, obj):
        """
        Add the object to the current database session (self.__session)
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session (self.__session)
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """
        Create all tables in the database (feature of SQLAlchemy)
        (WARNING: all classes that inherit from Base must be imported
        before calling Base.metadata.create_all(engine))
        Create the current database session
        (self.__session) from the engine (self.__engine)
        by using a sessionmaker
        - the option expire_on_commit must be set to False ;
        and scoped_session - to make sure your Session is thread-safe
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)

    def close(self):
        """
        Close the current database session
        edited on flask project
        """
        self.__session.close()
