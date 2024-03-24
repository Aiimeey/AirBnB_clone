#!/usr/bin/python3
"""Console Module"""
import cmd
from models.base_model import *
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):
    """The command interpreter class for the AirBnB clone project"""
    prompt = "(hbnb) "

    def default(self, line):
        """Handle default commands."""
        clss_ = line.split(".")[0]
        try:
            clss = globals()[clss_]
        except KeyError:
            print("** class doesn't exist **")
            return

        if line == f"{clss.__name__}.all()":
            return self.do_all(f"{clss.__name__}")

        if line == f"{clss.__name__}.count()":
            return self.do_count(f"{clss.__name__}")

        match_show_destroy = re.match(rf'^({re.escape(clss_)})\.(show|destroy)'
                                      rf'\("([a-z\d-]+)"\)$', line)
        match = re.match(rf'^({re.escape(clss_)})\.update\("([a-z\d-]+)",'
                         rf'\s*"([a-zA-Z_]+)",\s*"([a-zA-Z_]+)"\)$', line)
        match_update = re.match(rf'^({re.escape(clss_)})\.update\("([a-z\d-]+)'
                                rf'",\s*(.*)\)$', line)

        if match_show_destroy:
            Id = line.split('"')[1]
            cmd = match_show_destroy.group(2)
            for key, value in storage.all().items():
                if Id in f"{value}":
                    if cmd == "show":
                        return self.do_show(f"{clss_} {Id}")
                    elif cmd == "destroy":
                        return self.do_destroy(f"{clss_} {Id}")

        elif match:
            return self.do_update(f"{clss.__name__} {match.group(2)} "
                                  f"{match.group(3)} {match.group(4)}")
        elif match_update:
            x = json.loads(match_update.group(3).replace("'", '"'))
            first_key, first_value = list(x.items())[0]
            second_key, second_value = list(x.items())[1]
            return self.do_update(f"{clss.__name__} {match_update.group(2)} "
                                  f"{first_key} {first_value} {second_key} "
                                  f"{second_value}")

        else:
            print("** no instance found **")

    def do_count(self, line):
        """Count the number of instances of a class"""

        if line:
            clss = line.split(".")[0]
            clss = globals()[clss]
        c = 0
        for obj in storage.all().values():
            if clss is not None and isinstance(obj, clss):
                c += 1
        print(c)

    def do_create(self, line):
        """ Create an item """
        if not line:
            print("** class name missing **")
            return

        clss = line.split()[0]
        try:
            clss = globals()[clss]
            new_instance = clss()
            new_instance.save()
            print(new_instance.id)
        except KeyError:
            print("** class doesn't exist **")
            return

    def do_show(self, line):
        """Prints the string representation of an instance based \
                on the class name and id
        """
        if line:
            liste = line.split()
            if len(liste) == 0:
                print("** class name missing **")
            elif liste[0] not in globals():
                print("** class doesn't exist **")
            elif len(liste) == 1:
                print("** instance id missing **")
            else:
                dict_temp = models.storage.all()
                key = f"{liste[0]}.{liste[1]}"
                if key in dict_temp:
                    print(dict_temp[key])
                else:
                    print("** no instance found **")
        else:
            print("** class name missing **")

    def do_quit(self, arg):
        """Quit command to exit the program
        """

        return True

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        if line:
            liste = line.split()
            if liste[0] not in globals():
                print("** class doesn't exist **")
            elif len(liste) == 1:
                print("** instance id missing **")
            else:
                dict_temp = models.storage.all()
                key = f"{liste[0]}.{liste[1]}"
                if key in dict_temp:
                    del dict_temp[key]
                    models.storage.save()
                else:
                    print("** no instance found **")
        else:
            print('** class name missing **')

    def do_all(self, line):
        """display all the instances"""
        if line:
            clss = line.split()[0]
            try:
                clss = globals()[clss]
            except KeyError:
                print("** class doesn't exist **")
                return
        else:
            clss = None

        data = []

        for obj in storage.all().values():
            if clss is None or isinstance(obj, clss):
                data.append(obj.__str__())
        print(data)

    def do_update(self, line):
        """ update an item """
        if not line:
            print("** class name missing **")
            return
        clss = line.split()[0]
        try:
            clss = globals()[clss]
        except KeyError:
            print("** class doesn't exist **")
            return

        if len(line.split()) < 2 or not line.split()[1]:
            print("** instance id missing **")
            return

        instance_id = line.split()[1]
        key = f"{clss.__name__}.{instance_id}"
        data = storage.all().get(key)

        if data is None:
            print("** no instance found **")
            return

        if len(line.split()) < 3 or not line.split()[2]:
            print("** attribute name missing **")
            return
        else:
            attribute_name = line.split()[2]

        if len(line.split()) < 4 or not line.split()[3]:
            print("** value missing **")
            return
        else:
            attribute_value = line.split()[3]

        if (attribute_name != "created_at" and
                attribute_name != "updated_at" and attribute_name != "id"):

            value = self.check(attribute_value)
            setattr(data, attribute_name, value)

            storage.save()

        if len(line.split()) > 4:
            attribute_name = line.split()[4]

            if not line.split()[5]:
                print("** value missing **")
                return
            else:
                attribute_value = line.split()[5]

                if (attribute_name != "created_at" and
                        attribute_name != "updated_at" and
                        attribute_name != "id"):

                    value = self.check(attribute_value)
                    setattr(data, attribute_name, value)

                    storage.save()

    def check(self, value):
        """method that check type of the value """
        if value.isdigit():
            Value = int(value)
        else:
            try:
                Value = float(value)
            except ValueError:
                Value = str(value).strip().replace('"', '').replace("'", '')

        return Value

    def do_EOF(self, arg):
        """ Exit the program """
        print()
        return True

    def emptyline(self):
        """Handles the emptylines"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
