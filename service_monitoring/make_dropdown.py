"""
Because questionaire demands that the choices information be given explicitely,
it complicated to automate the insertion of new apps to the dropdown.
The idea is to have a file where all information needed to process a new app,
can be written on, and, afer, the dropdown file would read it, and update the
information on it. But because it won't accept an iteration like:
'for i in apps, print i', we decided to make dynamical the production of the
file itself.
"""
import os
import subprocess

# import snoop
from dotenv import load_dotenv
from mysql.connector import Error, connect
from questionary import Separator

# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])
load_dotenv()


# @snoop
def db_call():
    """
    Makes the call to the db.
    """
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="services",
        )
        cur = conn.cursor()
        query = "SELECT unit_name FROM services"
        cur.execute(query)
        data = cur.fetchall()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data


# @snoop
def make_dropdown():
    """
    We go line by line, reconstructing the original
    structure of the file.
    """
    drop = os.getenv("DROP")
    data = db_call()

    with open(drop, "w") as d:
        d.write('"')
        d.write('"')
        d.write('"\n')
        d.write("Here we'll define the dropdown with\n")
        d.write("all the information options.\n")
        d.write('"')
        d.write('"')
        d.write('"\n')
        d.write("from __future__ import unicode_literals\n\n")
        d.write("import re\n")
        d.write("import subprocess\n")
        d.write("import sys\n\n")
        d.write("import click\n")
        d.write("import questionary\n")
        d.write("# import snoop\n")
        d.write("from questionary import Separator, Style\n\n")
        d.write("# @snoop\n")
        d.write("def dropdown():\n")
        d.write('    "')
        d.write('"')
        d.write('"\n')
        d.write("    We'll use Questionary's multiple choice option, to ask what information he wants.\n")
        d.write("    It was used variables to identify the questions strings, because this allows for a\n")
        d.write("    value, dependent on a series of 'if' statements, to be chosen from them. When I did\n")
        d.write("    the same without the loop, the value was always the last if clause value. It was also\n")
        d.write("    added the 'path' and 'units' values to their respective 'app' and 'resposta' variables,\n")
        d.write("    so that, when running 'main', all the necessary information is already processed.\n")
        d.write('    "')
        d.write('"')
        d.write('"\n\n')
        d.write("    custom_style_monitor = Style(\n")
        d.write("        [\n")
        d.write('            ("qmark", "fg:#8E806A bold"),\n')
        d.write('            ("question", "fg:#E0DDAA bold"),\n')
        d.write('            ("answer", "fg:#eeedde"),\n')
        d.write('            ("pointer", "fg:#BB6464 bold"),\n')
        d.write('            ("highlighted", "fg:#E5E3C9 bold"),\n')
        d.write('            ("selected", "fg:#94B49F bold"),\n')
        d.write('            ("separator", "fg:#ff5c8d"),\n')
        d.write('            ("instruction", "fg:#E4CDA7"),\n')
        d.write('            ("text", "fg:#F1E0AC bold"),\n')
        d.write("        ]\n")
        d.write("    )\n\n")
        d.write("    app = questionary.checkbox(\n")
        d.write('        "What app do you want to use?",\n')
        d.write('        qmark="[x]",\n')
        d.write('        pointer="++",\n')
        d.write("        style=custom_style_monitor,\n")
        d.write("        choices=[\n")
        for i in data:
            d.write(f"       '{i[0]}',\n")
        d.write("        'Other',\n")
        d.write("            Separator('----- EXIT -----'),\n")
        d.write("            'Exit'\n")
        d.write("        ]\n")
        d.write("    ).ask()\n\n")
        d.write("    if app == 'Other':\n")
        d.write("        app = questionary.text('What service do you want to see?', qmark='[x]', style=custom_style_monitor).ask()\n\n")
        d.write("    resposta = questionary.checkbox(\n")
        d.write('        "What do you want to see?",\n')
        d.write('        qmark="[x]",\n')
        d.write('        pointer="++",\n')
        d.write("        style=custom_style_monitor,\n")
        d.write("        choices=[\n")
        d.write('            Separator("----- INFORMATION -----"),\n')
        d.write("            'service_status',\n")
        d.write("            'service_logs',\n")
        d.write("            'timers',\n")
        d.write("            'active_services',\n")
        d.write('            Separator("----- SERVICE ACTIONS -----"),\n')
        d.write('            "stop_service",\n')
        d.write("            'edit_service',\n")
        d.write("            'start_service',\n")
        d.write("            Separator('----- GENERAL ACTIONS -----'),\n")
        d.write("            'delete_service',\n")
        d.write("            'create_service',\n")
        d.write("            'daemon_reload',\n")
        d.write("            'reset_failed',\n")
        d.write('            Separator("----- EXIT -----"),\n')
        d.write("            'Exit',\n")
        d.write("        ],\n")
        d.write("    ).ask()\n")
        d.write('    print(click.style(f"app: {app}, resposta: {resposta}", fg="bright_white", bold=True))\n')
        d.write("    response = [app, resposta]\n")
        d.write("    return response\n\n")
        d.write("if __name__ == '__main__':\n")
        d.write("    dropdown()")


if __name__ == "__main__":
    make_dropdown()
