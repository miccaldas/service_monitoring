"""
Here we'll define the dropdown with
all the information options.
"""
from __future__ import unicode_literals

import re
import subprocess
import sys

import click
import questionary
# import snoop
from questionary import Separator, Style

# @snoop
def dropdown():
    """
    We'll use Questionary's multiple choice option, to ask what information he wants.
    It was used variables to identify the questions strings, because this allows for a
    value, dependent on a series of 'if' statements, to be chosen from them. When I did
    the same without the loop, the value was always the last if clause value. It was also
    added the 'path' and 'units' values to their respective 'app' and 'resposta' variables,
    so that, when running 'main', all the necessary information is already processed.
    """

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

    ambit = questionary.confirm(
        'Is your question about a specific service?',
         qmark='[x]',
         default=False,
         auto_enter=False,
         style=custom_style_monitor,
    ).ask()

    if ambit:
        app = questionary.select(
            "What app do you want to use?",
            qmark="[x]",
            pointer="++",
            use_indicator=True,
            style=custom_style_monitor,
            choices=[
               'Pip',
               'Yay_Querying',
               Separator("----- EXIT -----"),
               'Exit'
            ]
        ).ask()
        resposta = questionary.checkbox(
            "What do you want to see?",
            qmark="[x]",
            pointer="++",
           style=custom_style_monitor,
           choices=[
               Separator("----- INFORMATION -----"),
               "See: Service_Status",
               "See: Service_Logs",
               Separator("----- ACTIONS -----"),
               "See: Delete_Service",
               "See: Create_Service",
               "See: Stop_Service",
               "See: Edit_Service",
               "See: Start_Service",
               "See: Daemon_Reload",
               "See: Reset_Failed",
               Separator("----- EXIT -----"),
               "Exit",
            ],
        ).ask()
        print(click.style(f"app: {app}, resposta: {resposta}", fg="bright_white", bold=True))
        response = [app, resposta]
        return response

    if ambit is False:
        generalist = questionary.checkbox(
            "What do you want to see?",
            qmark="[x]",
            pointer="++",
            style=custom_style_monitor,
            choices=[
                Separator("----- INFORMATION -----"),
                "See: Timers",
                "See: Active_Services",
                "See: Service_Logs",
                Separator("----- ACTIONS -----"),
                "See: Delete_Service",
                "See: Create_Service",
                Separator("----- EXIT -----"),
                "Exit",
            ],
        ).ask()
        print(click.style(f"generalist: {generalist}", fg="bright_white", bold=True))
        general = ["dummy_app", generalist, "dummy_service"]
        return general


if __name__ == '__main__':
    dropdown()