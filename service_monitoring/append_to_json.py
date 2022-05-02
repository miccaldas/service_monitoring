"""Asks for the information of the new service and appends the entry to the json file."""
from __future__ import unicode_literals

import json
import subprocess
import sys

import click
import isort  # noqa: F401
import questionary
import snoop
from making_dropdown_file import make_dropdown
from questionary import Style
from snoop import pp

subprocess.run(["isort", __file__])


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @logger.catch
# @snoop
def entry():
    """
    Where we'll collect from the user
    the new service values. Because the
    app units are stored by questionary
    as a string, we need to transform it
    in a list, spliting the units on the
    linebreak symbol.
    """

    json_file = "/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json"

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
        default=True,
        auto_enter=False,
    ).ask()

    if su:
        ap = questionary.text(
            "What is the app name?",
            qmark="[x]",
            instruction="Write 'none' if not applicable.",
            style=custom_style_monitor,
        ).ask()
        nm = questionary.text(
            "What is the name?",
            qmark="[x]",
            style=custom_style_monitor,
        ).ask()
        pth = questionary.text(
            "What is the app's path?",
            qmark="[x]",
            instruction="Write 'none' if not applicable.",
            style=custom_style_monitor,
        ).ask()
        nts = questionary.text(
            "What are the app's units?",
            qmark="[x]",
            multiline=True,
            style=custom_style_monitor,
        ).ask()
        unit_lst = nts.split("\n")
        info = [ap, nm, pth, unit_lst]
        dropinf = {"app": f"{info[0]}", "name": f"{info[1]}", "path": f"{info[2]}", "units": info[3]}
        with open(json_file, "r+") as f:
            data = json.load(f)
            data["dropinfo"].append(dropinf)
            f.seek(0)
            json.dump(data, f, indent=4)
        print(click.style(f"Added to the json file the service with the info: {dropinf}", fg="bright_white", bold=True))
    else:
        nm = questionary.text(
            "What is the name?",
            qmark="[x]",
            style=custom_style_monitor,
        ).ask()
        nts = questionary.text(
            "What is the unit's name?",
            qmark="[x]",
            style=custom_style_monitor,
        ).ask()
        with open(json_file, "r+") as f:
            data = json.load(f)
            for i in range(len(data["dropinfo"])):
                if nm == data["dropinfo"][i]["name"]:
                    data["dropinfo"][i]["units"].append(nts)
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    break
        print(click.style(f"Added to the service {nm} the unit {nts}", fg="bright_white", bold=True))


if __name__ == "__main__":
    entry()
