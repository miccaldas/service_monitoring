"""
Main module where the app is activated.
We'll call the module 'dropdown', get
the questions chosen by the user and
direct them to the proper methods,
in module 'answer_methods.'
"""
import json
import os
import subprocess
import sys

from answer_methods import Answers
from dropdown import dropdown

# import snoop
# from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])

drop_results = dropdown()

with open("dropdown_info.json", "r") as f:
    data = f.read()  # It has to be read(), not readlines(), because the latter is a list.
info = json.loads(data)


# @snoop
def answer_methods():
    """
    We'll clean the results of list
    'resposta', to get it ready for
    the main function.
    """

    methods = []
    for i in drop_results[1]:
        if ":" in i:
            meth = i.split(":")[1]
            metho = meth.strip()
            methos = f"{metho.lower()}"
            methods.append(methos)

    return methods


if __name__ == "__main__":
    answer_methods()


# @snoop
def main():
    """
    We'll collect the return value of
    'answer_methods', so as to have
    clean values with the name of
    the methods to be run.
    """

    methods = answer_methods()

    data = []
    for i in range(len(info["dropinfo"])):
        if drop_results[0] == info["dropinfo"][i]["name"]:
            data.append(info["dropinfo"][i]["app"])
            data.append(info["dropinfo"][i]["path"])
            data.append(info["dropinfo"][i]["units"])

    drop = data[0]
    path = data[1]
    units = data[2]

    if path != "none":
        os.chdir(path)

    ress = []
    answer = Answers(drop, units)
    for method in methods:
        res = f"answer.{method}()"
        ress.append(res)

    for task in ress:
        print("\n")
        print("---------------------------------------------------------------------------")
        print("\n")
        exec(task)

    if drop == "Exit":
        sys.exit()


if __name__ == "__main__":
    main()
