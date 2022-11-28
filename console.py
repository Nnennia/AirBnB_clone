#!/usr/bin/python3
"""The HBNB console(shell)"""
import re
import os
from parse import parse
import cmd
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Defines the airbnb clone interpreter"""
 #   intro = " Welcome to HBNB shell, Type help or ? to list commands.\n"
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity"
        "Review"
    }

    def default(self, arg):
        """Generates defaults for invalid syntaxes"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """ EOF signal to quit program """
        print("")
        return True

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

    def do_show(self, arg):
        """prints the representation of an instance
        based on the class name and id"""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """Delets an instance based on the class name and id"""
        arg1 = parse(arg)
        objdict = storage.all()
        if len(arg1) == 0:
            print("** class name missing **")
        elif arg1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg1[0], arg1[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(arg1[0], arg1[1])]
            storage.save()

    def do_all(self, arg):
        "Prints string representation of instances"
        arg1 = parse(arg)
        if len(arg1) > 0 and arg1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")

        obj1 = []
        for obj in storage.all().values():
            if len(arg1) > 0 and arg1[0] == obj.__class__.__name__:
                obj1.append(obj.__str__())
            elif len(arg1) == 0:
                obj1.append(obj.__str__())
        print(obj1)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_clear(self, arg):
        """Clears the screen"""
        os.system("cls")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
