#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
from os import getenv
"""
Update __init__.py: (models/__init__.py)

Add a conditional depending of the value of the environment variable HBNB_TYPE_STORAGE:
If equal to db:
    Import DBStorage class in this file
    Create an instance of DBStorage and store it in the variable storage
    (the line storage.reload() should be executed after this instantiation)
Else:
    Import FileStorage class in this file
    Create an instance of FileStorage and store it in the variable storage 
    (the line storage.reload() should be executed after this instantiation)
"""
storage_type = getenv("HBNB_TYPE_STORAGE")


if (storage_type == "db"):
    from models.engine.db_storage import DBStorage
    print("storage ype is db")
    storage = DBStorage()
    
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
