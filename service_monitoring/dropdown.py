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

    app = questionary.checkbox(
        "What app do you want to use?",
        qmark="[x]",
        pointer="++",
        style=custom_style_monitor,
        choices=[
       'pypi_updt.service',
       'pypi_updt.timer',
       'yay_querying.service',
       'clidiary_updt.service',
       'clidiary_updt.timer',
       'yay_querying.timer',
       'git_automate.timer',
       'git_automate.service',
       'old_project_watchdog.service',
       'old_project_watchdog.timer',
        'Other',
            Separator('----- EXIT -----'),
            'Exit'
        ]
    ).ask()

    if app == 'Other':
        app = questionary.text('What service do you want to see?', qmark='[x]', style=custom_style_monitor).ask()

    resposta = questionary.checkbox(
        "What do you want to see?",
        qmark="[x]",
        pointer="++",
        style=custom_style_monitor,
        choices=[
            Separator("----- INFORMATION -----"),
            'service_status',
            'service_logs',
            'timers',
            'active_services',
            Separator("----- SERVICE ACTIONS -----"),
            "stop_service",
            'edit_service',
            'start_service',
            Separator('----- GENERAL ACTIONS -----'),
            'delete_service',
            'create_service',
            'daemon_reload',
            'reset_failed',
            Separator("----- EXIT -----"),
            'Exit',
        ],
    ).ask()
    print(click.style(f"app: {app}, resposta: {resposta}", fg="bright_white", bold=True))
    response = [app, resposta]
    return response

if __name__ == '__main__':
    dropdown()