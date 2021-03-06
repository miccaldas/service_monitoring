"""
Because questionaire demands that the choices information be given explicitely,
it complicated our desire to automate the insertion of new apps to the process.
The idea is to have a file where all information needed to process a new app,
can be written on, and, afer, the dropdown file would read it, and update the
information on it. But because it won't accept an iteration like:
'for i in apps, print i', we decided to make dynamical the production of the
file itself. This way we can update a json file with information, run this
module, and a new and updated 'dropdown.py' is ready for use!
"""
import json
import subprocess

import isort  # noqa: F401
import snoop
from questionary import Separator

subprocess.run(["isort", __file__])


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def make_dropdown():
    """
    We go line by line, reconstructing the original
    structure of the file, stopping only when we
    create loops that will get information from the
    dropdown_info.json file.
    """

    info = "/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json"

    with open(info, "r") as f:
        data = f.read()  # It has to be read(), not readlines(), because the latter is a list.

    res = json.loads(data)

    drop = "/home/mic/python/service_monitoring/service_monitoring/dropdown.py"

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
        d.write("import isort  # noqa: F401\n")
        d.write("import questionary\n")
        d.write("# import snoop\n")
        d.write("from questionary import Separator, Style\n\n")
        d.write("subprocess.run(['isort', __file__])\n\n\n")
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
        d.write("    ambit = questionary.confirm(\n")
        d.write("        'Is your question about a specific service?',\n")
        d.write("         qmark='[x]',\n")
        d.write("         default=False,\n")
        d.write("         auto_enter=False,\n")
        d.write("    ).ask()\n\n")
        d.write("    if ambit:\n")
        d.write("        app = questionary.select(\n")
        d.write('            "What app do you want to use?",\n')
        d.write('            qmark="[x]",\n')
        d.write('            pointer="++",\n')
        d.write("            use_indicator=True,\n")
        d.write("            style=custom_style_monitor,\n")
        d.write("            choices=[\n")
        for i in range(len(res["dropinfo"])):
            d.write(f"               '{res['dropinfo'][i]['name']}',\n")
        d.write('               Separator("----- EXIT -----"),\n')
        d.write("               'Exit'\n")
        d.write("            ]\n")
        d.write("        ).ask()\n")
        d.write("        resposta = questionary.checkbox(\n")
        d.write('            "What do you want to see?",\n')
        d.write('            qmark="[x]",\n')
        d.write('            pointer="++",\n')
        d.write("           style=custom_style_monitor,\n")
        d.write("           choices=[\n")
        d.write('               Separator("----- CELERY INFORMATION -----"),\n')
        d.write('               "See: Clock",\n')
        d.write('               "See: Scheduled",\n')
        d.write('               "See: Stats",\n')
        d.write('               "See: Reports",\n')
        d.write('               "See: Events",\n')
        d.write('               Separator("----- SYSTEMD INFORMATION -----"),\n')
        d.write('               "See: Service_Status",\n')
        d.write('               "See: Service_Logs",\n')
        d.write('               Separator("----- SYSTEMD ACTIONS -----"),\n')
        d.write('               "See: Delete_Service",\n')
        d.write('               "See: Create_Service",\n')
        d.write('               "See: Stop_Service",\n')
        d.write('               "See: Edit_Service",\n')
        d.write('               "See: Start_Service",\n')
        d.write('               "See: Daemon_Reload",\n')
        d.write('               "See: Reset_Failed",\n')
        d.write('               Separator("----- EXIT -----"),\n')
        d.write('               "Exit",\n')
        d.write("            ],\n")
        d.write("        ).ask()\n")
        d.write('        print(click.style(f"app: {app}, resposta: {resposta}", fg="bright_white", bold=True))\n')
        d.write("        response = [app, resposta]\n")
        d.write("        return response\n\n")
        d.write("    if ambit is False:\n")
        d.write("        generalist = questionary.checkbox(\n")
        d.write('            "What do you want to see?",\n')
        d.write('            qmark="[x]",\n')
        d.write('            pointer="++",\n')
        d.write("            style=custom_style_monitor,\n")
        d.write("            choices=[\n")
        d.write('                Separator("----- CELERY INFORMATION -----"),\n')
        d.write('                "See: Active_Nodes",\n')
        d.write('                Separator("----- SYSTEMD INFORMATION -----"),\n')
        d.write('                "See: Timers",\n')
        d.write('                "See: Active_Services",\n')
        d.write('                "See: Service_Logs",\n')
        d.write('                Separator("----- SYSTEMD ACTIONS -----"),\n')
        d.write('                "See: Delete_Service",\n')
        d.write('                "See: Create_Service",\n')
        d.write('                Separator("----- EXIT -----"),\n')
        d.write('                "Exit",\n')
        d.write("            ],\n")
        d.write("        ).ask()\n")
        d.write('        print(click.style(f"generalist: {generalist}", fg="bright_white", bold=True))\n')
        d.write('        general = ["dummy_app", generalist, "dummy_service"]\n')
        d.write("        return general\n\n\n")
        d.write("if __name__ == '__main__':\n")
        d.write("    dropdown()")


if __name__ == "__main__":
    make_dropdown()
