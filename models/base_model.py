#!/usr/bin/python3
"""The Base model class"""
# import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Defines all common atributes/methods for other classes"""

    def __init__(self, *args, **kwargs) -> None:
        """Initalize a new base model"""
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, tform)
                else:
                    self.__dict__[key] = value
        # else:
        #  #   models.storage.new(self)

    def save(self):
        """updates the public instance attribute updated_at"""
        self.updated_at = datetime.now()
        # models.storage.new(self)

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


my_model = BaseModel()
my_model.name = "My First Model"
my_model.my_number = 89
print(my_model)
my_model.save()
print(my_model)
my_model_json = my_model.to_dict()
print(my_model_json)
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))
