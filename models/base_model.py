#!/usr/bin/python3
"""The Base model class"""
import models
import uuid
import datetime


class BaseModel:
    """Defines all common atributes/methods for other classes"""

    def __init__(self, *args, **kwargs) -> None:
        """Initalize a new base model"""
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.datetime.strptime
                    (value, tform)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """updates the public instance attribute updated_at"""
        self.updated_at = datetime.datetime.now()
        models.storage.new(self)

    def to_dict(self):
        """returns a dictionary containing all keys/
        values of __dict__ of the insance"""
        dict = self.__dict__.copy()
        dict["create_at"] = self.created_at.isoformat()
        dict["updated_at"] = self.updated_at.isoformat()
        dict["__class__"] = self.__class__.__name__
        return dict

    def __str__(self) -> str:
        """prints the class name, self.id and self.dict"""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
