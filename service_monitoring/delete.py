"""
Module to delete Systemd's services and correspondent database entries.
"""
import os
import subprocess

import questionary
import snoop
from dotenv import load_dotenv
from mysql.connector import Error, connect
from questionary import Separator, Style
from rich import text
from rich.console import Console
from rich.table import Table

from service_monitoring.make_dropdown import make_dropdown

# from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])

load_dotenv()
console = Console(width=960)


# @snoop
def dbdelunit(selunit):
    """
    Deletes a unit in a service in the database.
    """
    for sel in selunit:
        delcmd = f"DELETE FROM services WHERE id = {sel}"
        dbcommit(delcmd)

    console.print(f"  <X> - The {selunit} unit(s) were deleted.", style="bold #E2C275")


# @snoop
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

    console.print(
        f"  <X> - The {delservices} services were deleted from Systemctl.",
        style="bold #E2C275",
    )


# @snoop
def dbfetch(query):
    """
    Gets info from the database.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="services")
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data


# @snoop
def dbcommit(query):
    """
    Sends info to the database.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="services")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    console.print(f"  The query {query} was run.", style="bold #E2C275")


# @snoop
def delete():
    """
    Called by 'main'. From information from id's and unit_names,
    we'll delete by unit_name, first in Systemctl by the name
    of the service's, then by id's in the database.
    """

    # First we get information to identify the rows to delete.
    query = "SELECT id, name, unit_name FROM services"
    # Make a db call.
    data = dbfetch(query)
    # We print the output, so the user can choose ehat to delete.
    for i in data:
        console.print(f"  {i[0]} - {i[1]} - {i[2]}", style="bold #939B62", justify="left")
        # print("\n")
    delchoice = console.input("[bold #E2C275]  { X } - Choose the id's you want: [/]")
    # In case we were given more than one id, we seprate them by space.
    selunit = delchoice.split(" ")
    # This converts the id's into strings, which won't do. We turn them
    # back to ints.
    delints = [int(i) for i in selunit]
    # Build a list of unit_names, names, to use when deleting in Systemctl.
    delservices = [i[2] for i in data if i in delints]
    # Call the function to delete Systemctl's services.
    systemctldel(delservices)
    # Call function to delete database entries.
    dbdelunit(delints)
    # We redraw the app's presentation, with the updated number of entries.
    make_dropdown()


if __name__ == "__main__":
    delete()
