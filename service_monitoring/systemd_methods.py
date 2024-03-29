"""
Module that houses a class that encompasses
all the methods that'll create the answers
to the questionnaire questions.
"""

import os
import subprocess
from contextlib import suppress

import click
import questionary

# import snoop
from dotenv import load_dotenv
from mysql.connector import Error, connect
from questionary import Separator, Style

from service_monitoring.create_service import maincreate
from service_monitoring.delete import delete

# from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


load_dotenv()
monitor = os.getenv("MONITOR")

# snoop.install(watch_extras=[type_watch])

custom_style_monitor = Style(
    [
        ("qmark", "fg:#ff5c8d bold"),
        ("question", "fg:#E0DDAA bold"),
        ("pointer", "fg:#BB6464 bold"),
        ("highlighted", "fg:#E5E3C9 bold"),
        ("selected", "fg:#94B49F bold"),
        ("text", "fg:#F1E0AC bold"),
    ]
)


class Answers:
    """
    This class houses all the actions that the user chooses.
    Each one is a command to be executed or a script to be run.
    It needs two values to be instantiated:

    :param str who: Chooses what method to implement.
    """

    def __init__(self, who):
        self.who = who

    # @snoop
    def sbproc(self, cmd):
        """
        Concentrate all subprocess calls in a single function.
        """
        subprocess.run(cmd, shell=True)

    # @snoop
    def db_commit(self, query_commit):
        """
        Makes db calls where the aim is to commit to the db.
        """
        try:
            conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="services",
            )
            cur = conn.cursor()
            cur.execute(query_commit)
            conn.commit()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

    # @snoop
    def db_getdata(self, query_data):
        """
        Makes db calls where the aim is to fetch data.
        """
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="services")
            cur = conn.cursor()
            cur.execute(query_data)
            data = cur.fetchall()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

        return data

    # @snoop
    def timers(self):
        """
        Shows active *Systemd* timers.
        This method runs the following command::

           sudo systemctl --no-pager list-timers
        """
        self.sbproc("sudo systemctl --no-pager list-timers")

    # @snoop
    def active_services(self):
        """
        Shows active *Systemd* services.\n
        This method runs the following command::

           sudo systemctl --no-pager --type=service
        """
        self.sbproc("sudo systemctl --no-pager list-timers")

    # @snoop
    def service_status(self):
        """
        See *Systemd* services status.\n
        Requires a *who* value.\n
        This method runs the following command::

           sudo systemctl --no-pager -l status <service>
        """
        for w in self.who:
            cmd8 = f"systemctl --no-pager status {w}"
            self.sbproc(cmd8)
            print("\n")
        print("\n\n")

    # @snoop
    def service_logs(self):
        """
        See logs for specific *Systemd* services.

        :var str choice: User input. Asks if he wants to see the services belonging to the current *who* value.

        If yes, it runs the following command::

            sudo SYSTEMD_COLORS=1 journalctl | grep <service>\n
        If no, it assumes the user wants to have a general view of the
        processes, and runs the command::

            sudo SYSTEMD_COLORS=1 journalctl | grep python3
        """
        for w in self.who:
            cmd9 = f"sudo SYSTEMD_COLORS=1 journalctl -u {w} -S '1 hour ago'"
            self.sbproc(cmd9)
            print("\n")
        print("\n\n")

    # @snoop
    def disable_service(self):
        """
        Disables systemctl service.
        """
        for w in self.who:
            cmd30 = f"sudo systemctl disable {w}"
            self.sbproc(cmd30)

    # @snoop
    def enable_service(self):
        """
        Enables systemctl service.
        """
        for w in self.who:
            cmd30 = f"sudo systemctl enable {w}"
            self.sbproc(cmd30)

    # @snoop
    def stop_service(self):
        """
        Stops execution of *Systemd* services.

        Requires a *who* value.

        Runs the following command::

           sudo systemctl stop <service>
        """
        for w in self.who:
            cmd10 = f"sudo systemctl stop {w}"
            self.sbproc(cmd10)
        print("\n\n")

    # @snoop
    def start_service(self):
        """
        Starts *Systemd* service.

        Requires a *who* value.

        Runs the following command::

            sudo systemctl start <service>
        """
        for w in self.who:
            cmd11 = f"sudo systemctl start {w}"
            self.sbproc(cmd11)
        print("\n\n")

    # @snoop
    def daemon_reload(self):
        """
        Reloads the daemons of all services and timers.

        Necessary after any alteration to the *Systemd* services.

        Runs the following command::

            sudo systemctl daemon-reload
        """
        self.sbproc("sudo systemctl daemon-reload")

    # @snoop
    def edit_service(self):
        """
        Stops the units, opens the service or timer in *$EDITOR*, reloads *Systemmd* daemon and restarts units.

        Requires a *who* value.

        Runs the following commands in succession::

            sudo systemctl stop <service>
            sudo vim /usr/lib/systemd/system/<service>
            sudo systemctl daemon-reload
            sudo systemctl start <service>
        """
        for w in self.who:
            cmd10 = f"sudo systemctl stop {w}"
            self.sbproc(cmd10)
            cmd12 = f"sudo vim '/usr/lib/systemd/system/{w}'"
            self.sbproc(cmd12)
            cmd13 = "sudo systemctl daemon-reload"
            self.sbproc(cmd13)
            cmd11 = f"sudo systemctl start {w}"
            self.sbproc(cmd11)

    # @snoop
    def reset_failed(self):
        """
        After deleting units, run this command to have Systemd erase them.\n
        If you don't, it will complain that it can't find the unit.

        Runs the following command::

            sudo systemctl reset-failed
        """
        self.sbproc("sudo systemctl reset-failed")

    # @snoop
    def delete_service(self):
        """
        Call external function which deletes a service.
        """
        delete()

    # @snoop
    def create_service(self):
        """
        Calls external function who creates a systemd service.
        """
        maincreate()

    # @snoop
    def Exit(self):
        """
        Exits the user from any of the dropdowns.
        """
        with suppress(KeyboardInterrupt):
            raise SystemExit()
