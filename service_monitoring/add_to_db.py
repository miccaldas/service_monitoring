"""Asks for the information of the new service and appends the data to the db."""
from __future__ import unicode_literals

import os
import subprocess

import click
import questionary
import snoop
from dotenv import load_dotenv
from mysql.connector import Error, connect
from questionary import Style
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])
load_dotenv()


@snoop
def db_call(query):
    """
    Makes db calls.
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


@snoop
def entry():
    """
    Where we'll collect from the user the new service values.
    Because the app units are stored by questionary as a string,
    we need to transform it to list, spliting the units on the
    linebreak symbol.\n
    :var str su: User choice. Asks if a new service was created.\n
    :var str nm: Asked if *su* was positive. User choice. What is the service name?
    :var str nts: Asked if *su* was positive. User choice. What are its services?\n
    """

    info = os.getenv("DROPINFO")

    custom_style_monitor = Style(
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

    su = questionary.confirm(
        "Did you created a new service?",
        qmark="[x]",
        auto_enter=False,
    ).ask()
    if su:
        nm = questionary.text(
            "What is the name?",
            qmark="[x]",
            style=custom_style_monitor,
        ).ask()
        serv = questionary.text(
            "What is the service's unit_name?",
            default="None",
            qmark="[x]",
            style=custom_style_monitor,
        ).ask()
        tim = questionary.text(
            "What is the timer's unit_name?",
            qmark="[x]",
            default="None",
            style=custom_style_monitor,
        ).ask()
        new_service = [nm, serv, tim]
        # Updates the db with new service.
        query = f"INSERT INTO services (name, unit_name, unit_type) VALUES('{nm}', '{serv}', 'service'), ('{nm}', '{tim}', 'timer')"
        db_call(query)
    else:
        nam = questionary.text(
            "What is the name of the service?",
            qmark="[x]",
            style=custom_style_monitor,
        ).ask()
        nts = questionary.select(
            "What kind of unit did you create?",
            choices=["timer", "service"],
            qmark="[x]",
            style=custom_style_monitor,
        ).ask()
        newunit = questionary.text("What is the name of the unit?", qmark="[x]", style=custom_style_monitor).ask()
        # Updates db with altered service.
        query1 = f"UPDATE {nts} SET unit_name = {newunit} WHERE name = {nam}"
        db_call(query1)

        print(
            click.style(
                f"Added the unit {newunit} to the service {nam}",
                fg="bright_white",
                bold=True,
            )
        )


if __name__ == "__main__":
    entry()
