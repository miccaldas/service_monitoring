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

import snoop
from snoop import pp

from service_monitoring.answer_methods import Answers
from service_monitoring.dropdown import dropdown


def type_watch(source, value):
    return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])

dropdown = list(dropdown())

with open(
    "/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json", "r"
) as f:
    servs = (
        f.read()
    )  # It has to be read(), not readlines(), because the latter is a list.
info = json.loads(servs)


# @snoop
def answer_methods():
    """
    We'll clean the results of list
    'resposta', to get it ready for
    the main function.
    """

    methods = []
    for i in dropdown[1]:
        if ":" in i:
            meth = i.split(":")[1]
            metho = meth.strip()
            methos = f"{metho.lower()}"
            methods.append(methos)

    return methods


# @snoop
def main():
    """
    We'll collect the return value of
    'answer_methods', so as to have
    clean values with the name of
    the methods to be run.
    """

    methods = answer_methods()

    if "dummy_service" not in dropdown:
        for i in dropdown:
            if i == "Exit":
                sys.exit()
        data = []
        for i in range(len(info["dropinfo"])):
            if dropdown[0] == info["dropinfo"][i]["name"]:
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
                    print(
                        "---------------------------------------------------------------------------"
                    )
                    print("\n")
                    exec(task)
    else:
        drop = dropdown[0]
        if drop == "Exit":
            sys.exit()
        units = dropdown[2]
        ress = []
        answer = Answers(drop, units)
        for method in methods:
            res = f"answer.{method}()"
            ress.append(res)
            for task in ress:
                print("\n")
                print(
                    "---------------------------------------------------------------------------"
                )
                print("\n")
                exec(task)


if __name__ == "__main__":
    main()
