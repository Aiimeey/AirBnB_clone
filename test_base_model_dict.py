#!/usr/bin/python3
import inspect
import io
import sys
import cmd
import shutil

"""
 Cleanup file storage
"""
import os
file_path = "file.json"
if not os.path.exists(file_path):
    try:
        from models.engine.file_storage import FileStorage
        file_path = FileStorage._FileStorage__file_path
    except:
        pass
if os.path.exists(file_path):
    os.remove(file_path)

"""
 Backup console file
"""
if os.path.exists("tmp_console_main.py"):
    shutil.copy("tmp_console_main.py", "console.py")
shutil.copy("console.py", "tmp_console_main.py")

"""
 Updating console to remove "__main__"
"""
with open("tmp_console_main.py", "r") as file_i:
    console_lines = file_i.readlines()
    with open("console.py", "w") as file_o:
        in_main = False
        for line in console_lines:
            if "__main__" in line:
                in_main = True
            elif in_main:
                if "cmdloop" not in line:
                    file_o.write(line.lstrip("    ")) 
            else:
                file_o.write(line)

import console

"""
 Create console
"""
console_obj = "HBNBCommand"
for name, obj in inspect.getmembers(console):
    if inspect.isclass(obj) and issubclass(obj, cmd.Cmd):
        console_obj = obj

my_console = console_obj(stdout=io.StringIO(), stdin=io.StringIO())
my_console.use_rawinput = False

"""
 Exec command
"""
def exec_command(my_console, the_command, last_lines = 1):
    my_console.stdout = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = my_console.stdout
    my_console.preloop()
    the_command = my_console.precmd(the_command)
    my_console.onecmd(the_command)
    sys.stdout = real_stdout
    lines = my_console.stdout.getvalue().split("\n")
    return "\n".join(lines[(-1*(last_lines+1)):-1])

"""
 Tests
"""
model_class = "Amenity"
attribute_name = "attribute_name"
attribute_value = 89
result = exec_command(my_console, "create {}".format(model_class))
if result is None or result == "":
    print("FAIL: No ID retrieved")
    
model_id = result


def model_has_attribute(my_console, model_class, model_id, attr_name, attr_val):
    is_found = False    
    result = exec_command(my_console, "show {} {}".format(model_class, model_id))
    if result is None or result == "":
        pass  
    elif model_id in result and "id" in result and attr_name in result and str(attr_val) in result:
        is_found = True
    print(is_found)
    return is_found

result = exec_command(my_console, "{}.update(\"{}\", \"{}\", \"{}\")".format(model_class, model_id, attribute_name, attribute_value))
print(exec_command(my_console,"all"))
print(my_console, "{}.update(\"{}\", \"{}\", \"{}\")".format(model_class, model_id, attribute_name, attribute_value))
if not model_has_attribute(my_console, model_class, model_id, attribute_name, attribute_value):

    result = exec_command(my_console, "{}.update({}, \"{}\", \"{}\")".format(model_class, model_id, attribute_name, attribute_value))
    print(my_console, "{}.update({}, \"{}\", \"{}\")".format(model_class, model_id, attribute_name, attribute_value))
    if not model_has_attribute(my_console, model_class, model_id, attribute_name, attribute_value):
        result = exec_command(my_console, "{}.update(\"{}.{}\", \"{}\", \"{}\")".format(model_class, model_class, model_id, attribute_name, attribute_value))
        print(my_console, "{}.update(\"{}.{}\", \"{}\", \"{}\")".format(model_class, model_class, model_id, attribute_name, attribute_value))
    if not model_has_attribute(my_console, model_class, model_id, attribute_name, attribute_value):
        result = exec_command(my_console, "{}.update({}.{}, \"{}\", \"{}\")".format(model_class, model_class, model_id, attribute_name, attribute_value))
        print(my_console, "{}.update({}.{}, \"{}\", \"{}\")".format(model_class, model_class, model_id, attribute_name, attribute_value))    
if not model_has_attribute(my_console, model_class, model_id, attribute_name, attribute_value):
    print("FAIL: model doesn't have new attribute")
    
print("OK", end="")

shutil.copy("tmp_console_main.py", "console.py")