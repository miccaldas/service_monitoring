"""
Here we'll define the dropdown with
all the information options.
"""
from __future__ import unicode_literals

import re
import subprocess
import sys

import click
import isort  # noqa: F401
import questionary
# import snoop
from questionary import Separator, Style

subprocess.run(["isort", __file__])


# @snoop
def dropdown():
    """
    We present the user with a dropdown with a list of functionalities, wait for him to choose one and register the choice.

    :var str ambit: User input. *Is you question about a specific service?*
    :var str app: If ambit. User input. *What app do you want to use?*
    :var str resposta: If ambit. User input. *What do you want to see?* Shows Answers methods.
    :var str generalist: If not ambit. User input. *What do you want to see?* Shows generic methods.

    Options:\n
    *See: Clock* - :meth:`Answers.clock`\n
    *See: Scheduled* - :meth:`Answers.scheduled`\n
    *See: Stats* - :meth:`Answers.stats`\n
    *See: Reports* - :meth:`Answers.reports`\n
    *See: Events* - :meth:`Answers.events`\n
    *See: Service Status* - :meth:`Answers.service_status`\n
    *See: Service Logs* - :meth:`Answers.service_logs`\n
    *See: Delete Service* - :meth:`Answers.delete_service`\n
    *See: Create Service* - :meth:`Answers.create_service`\n
    *See: Stop Service* - :meth:`Answers.create_service`\n
    *See: Edit Service* - :meth:`Answers.edit_service`\n
    *See: Start Service* - :meth:`Answers.start_service`\n
    *See: Daemon Reload* - :meth:`Answers.daemon_reload`\n
    *See: Reset Failed* - :meth:`Answers.reset_failed`\n
    *Exit* - *sys.exit()*
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
        "Is your question about a specific service?",
        qmark="[x]",
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
                "Flower",
                "Pip",
                "Yay Querying",
                "Bkmks Cleaning",
                Separator("----- EXIT -----"),
                "Exit",
            ],
        ).ask()
        resposta = questionary.checkbox(
            "What do you want to see?",
            qmark="[x]",
            pointer="++",
            style=custom_style_monitor,
            choices=[
                Separator("----- CELERY INFORMATION -----"),
                "See: Clock",
                "See: Scheduled",
                "See: Stats",
                "See: Reports",
                "See: Events",
                Separator("----- SYSTEMD INFORMATION -----"),
                "See: Service_Status",
                "See: Service_Logs",
                Separator("----- SYSTEMD ACTIONS -----"),
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
                Separator("----- CELERY INFORMATION -----"),
                "See: Active_Nodes",
                Separator("----- SYSTEMD INFORMATION -----"),
                "See: Timers",
                "See: Active_Services",
                "See: Service_Logs",
                Separator("----- SYSTEMD ACTIONS -----"),
                "See: Delete_Service",
                "See: Create_Service",
                Separator("----- EXIT -----"),
                "Exit",
            ],
        ).ask()
        print(click.style(f"generalist: {generalist}", fg="bright_white", bold=True))
        general = ["dummy_app", generalist, "dummy_service"]
        return general


if __name__ == "__main__":
    dropdown()
