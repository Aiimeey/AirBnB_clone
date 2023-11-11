#!/usr/bin/python3
"""Console Module"""
import cmd
from models.base_model import *
from models.user import User
from models import storage


class HBNBCommand(cmd.Cmd):
    """The command interpreter class for the AirBnB clone project"""
    prompt = "(hbnb) "

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
        """Printsallstring representationofallinstancesbased on/nor class name
        """
        liste = []
        dic_temp = models.storage.all()
        for i in dic_temp.values():
            liste.append(str(i))
        if line:
            if line not in globals():
                print("** class doesn't exist **")
            else:
                print(liste)
        else:
            print(liste)

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

    def check(self, value):
        """method that check type of the value """
        if '"' or "'" in value:
            Value = str(value)
        elif value.isdigit():
            Value = int(value)
        else:
            try:
                Value = float(value)
            except ValueError:
                Value = str(value)

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
