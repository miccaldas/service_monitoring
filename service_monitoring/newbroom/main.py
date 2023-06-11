"""
Module Docstring
"""
import os
from contextlib import suppress

import questionary
import snoop
from blessed import Terminal
from dotenv import load_dotenv
from questionary import Separator, Style
from snoop import pp

from delete import delete


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


# @snoop
def main():
    """"""
    term = Terminal()
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
    task = questionary.checkbox(
        "What do you want to do?",
        choices=["Delete", "Exit"],
        qmark="[x]",
        style=cstyle,
    ).ask()

    if task[0] == "Delete":
        delete()
    if task[0] == "Exit":
        with suppress(KeyboardInterrupt, IndexError):
            raise SystemExit


if __name__ == "__main__":
    main()
