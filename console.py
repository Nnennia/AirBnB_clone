#!/usr/bin/python3
import cmd
from models import storage
from parse import parse
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    intro = " Welcome to HBNB shell, Type help or ? to list commands.\n"
    prompt: str = "(hbnb)"

    def do_quit(self, *args):
        """Quit command to exit the program"""
        return True

    do_EOF = do_quit

    def emptyline(self):
        """Empty line should do nothing when executed"""
        pass

    def do_create(self, arg):
        """Creates new class instance and prints the id"""
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist")
        else:
            print(eval(argl[0])().id)
            storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
