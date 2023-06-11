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
from contextlib import suppress

import snoop
from dotenv import load_dotenv
from mysql.connector import Error, connect
from snoop import pp

from service_monitoring.answer_methods import Answers
from service_monitoring.dropdown import dropdown

load_dotenv()
monitor = os.getenv("MONITOR")


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

dropdown = list(dropdown())


@snoop
def db_call():
    """
    Makes calls to the db.
    """
    try:
        conn = connect(
            host="localhost", user="mic", password="xxxx", database="services"
        )
        cur = conn.cursor()
        query = "SELECT * FROM services"
        cur.execute(query)
        data = cur.fetchall()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data


@snoop
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


@snoop
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
                raise SystemExit
        data = db_call()
        for i in data:
            if dropdown[0] == i[1]:
                drop = data[0]
                if i[3] == "service":
                    service = i[2]
                else:
                    service = "None"
                if i[3] == "timer":
                    timer = i[2]
                else:
                    timer = "None"
                units = (service, timer)
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
        definemethods(methods)


@snoop
def definemethods(methods):
    drop = dropdown[0]
    if drop == "Exit":
        with suppress(KeyboardInterrupt):
            raise SystemExit
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
