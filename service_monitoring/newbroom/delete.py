"""
Module Docstring
"""
import os
import subprocess

import questionary
import snoop
from dotenv import load_dotenv
from mysql.connector import Error, connect
from questionary import Separator, Style
from service_monitoring.make_dropdown import make_dropdown
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


@snoop
def dbdelunit(selunit):
    """
    Deletes a unit in a service in the database.
    """
    for sel in selunit:
        delcmd = f"DELETE FROM services WHERE id = {sel}"
        dbcommit(delcmd)

    print("The {selunit} unit(s) were deleted.")


@snoop
def systemctldel(delservices):
    """
    Deletes services or timers
    from systemctl.
    """
    for sel in delservices:
        a = (f"sudo systemctl stop {sel}",)
        b = (f"sudo systemctl disable {sel}",)
        c = ("sudo systemctl daemon-reload",)
        d = (f"sudo trash /usr/lib/systemd/system/{sel}",)
        e = "sudo systemctl reset-failed"

        for cmd in [a, b, c, d, e]:
            subprocess.run(cmd, shell=True)

    print(f"The {delservices} services were deleted from Systemctl")


@snoop
def dbfetch(query):
    """
    Gets info from the database.
    """

    try:
        conn = connect(
            host="localhost", user="mic", password="xxxx", database="services"
        )
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data


@snoop
def dbcommit(query):
    """
    Sends info to the database.
    """

    try:
        conn = connect(
            host="localhost", user="mic", password="xxxx", database="services"
        )
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    print(f"The query {query} was run.")


@snoop
def delete():
    """"""
    cstyle = Style(
        [
            ("qmark", "fg:#8E806A bold"),
            ("question", "fg:#E0DDAA bold"),
            ("answer", "fg:#eeedde"),
            ("pointer", "fg:#BB6464 bold"),
            ("highlighted", "fg:#E5E3C9 bold"),
            ("selected", "fg:#94B49F bold"),
            ("separator", "fg:#ff5c8d"),
            ("instruction", "fg:#E4CDA7"),
            ("text", "fg:#F1E0AC bold"),
        ]
    )

    query = "SELECT id, name, unit_name FROM services"
    data = dbfetch(query)
    for i in data:
        print(f"{i[0]} - {i[1]} - {i[2]}")
        print("\n")
    delchoice = input("Choose the id's you want. ")
    selunit = delchoice.split(" ")
    delints = [int(i) for i in selunit]
    delservices = [i[2] for i in data if i in delints]
    systemctldel(delservices)
    dbdelunit(delints)
    make_dropdown()


if __name__ == "__main__":
    delete()
