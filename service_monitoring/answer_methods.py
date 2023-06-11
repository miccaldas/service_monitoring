"""
Module that houses a class that encompasses
all the methods that'll create the answers
to the questionnaire questions.
"""

import json
import os
import re
import subprocess
from contextlib import suppress
from time import sleep

import click
import questionary
import snoop
from dotenv import load_dotenv
from mysql.connector import Error, connect
from questionary import Separator, Style
from snoop import pp

from service_monitoring.add_to_db import entry
from service_monitoring.make_dropdown import make_dropdown


def type_watch(source, value):
    return "type({})".format(source), type(value)


load_dotenv()
monitor = os.getenv("MONITOR")

snoop.install(watch_extras=[type_watch])

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

    :param str drop: What application do we want to use?
    :param str units: Chooses what method to implement.
    """

    def __init__(self, drop, units):
        self.drop = drop
        self.units = units

    @snoop
    def sbproc(self, cmd):
        """
        Concentrate all subprocess calls in a single function.
        """
        subprocess.run(cmd, shell=True)

    @snoop
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

    @snoop
    def db_getdata(self, query_data):
        """
        Makes db calls where the aim is to fetch data.
        """
        try:
            conn = connect(
                host="localhost", user="mic", password="xxxx", database="services"
            )
            cur = conn.cursor()
            cur.execute(query_data)
            data = cur.fetchall()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

        return data

    @snoop
    def timers(self):
        """
        Shows active *Systemd* timers.
        This method runs the following command::

           sudo systemctl --no-pager list-timers
        """
        self.sbproc("sudo systemctl --no-pager list-timers")

    @snoop
    def active_services(self):
        """
        Shows active *Systemd* services.\n
        This method runs the following command::

           sudo systemctl --no-pager --type=service
        """
        self.sbproc("sudo systemctl --no-pager list-timers")

    @snoop
    def service_status(self):
        """
        See *Systemd* services status.\n
        Requires a *unit* value.\n
        This method runs the following command::

           sudo systemctl --no-pager status <service>
        """
        for unit in self.units:
            cmd8 = f"systemctl --no-pager status {unit}"
            self.sbproc(cmd8)
            print("\n\n")

    @snoop
    def service_logs(self):
        """
        See logs for specific *Systemd* services.

        :var str choice: User input. Asks if he wants to see the services belonging to the current *unit* value.

        If yes, it runs the following command::

            sudo SYSTEMD_COLORS=1 journalctl | grep <service>\n
        If no, it assumes the user wants to have a general view of the
        processes, and runs the command::

            sudo SYSTEMD_COLORS=1 journalctl | grep python3
        """
        units = [str(i) for i in self.units]
        if "dummy_service" not in self.units:
            for unit in units:
                choice = input(
                    click.style(
                        f"[*] - Do you want to see logs for {unit}? [y/n] ",
                        fg="bright_green",
                        bold=True,
                    )
                )
                if choice == "y":
                    cmd9 = (
                        f"sudo SYSTEMD_COLORS=1 journalctl -u {choice} -S '1 hour ago'"
                    )
                    self.sbproc(cmd9)
                    print("\n\n")
        else:
            self.sbproc("sudo SYSTEMD_COLORS=1 journalctl | grep python3")
        self.sbproc("sudo systemctl --no-pager list-timers")

    @snoop
    def disable_service(self):
        """
        Disables systemctl service.
        """
        for unit in self.units:
            cmd30 = f"sudo systemctl disable {unit}"
            self.sbproc(cmd30)

    @snoop
    def stop_service(self):
        """
        Stops execution of *Systemd* services.

        Requires a *unit* value.

        Runs the following command::

           sudo systemctl stop <service>
        """
        for unit in self.units:
            cmd10 = f"sudo systemctl stop {unit}"
            self.sbproc(cmd10)
            print("\n\n")

    @snoop
    def start_service(self):
        """
        Starts *Systemd* service.

        Requires a *unit* value.

        Runs the following command::

            sudo systemctl start <service>
        """
        for unit in self.units:
            cmd11 = f"sudo systemctl start {unit}"
            self.sbproc(cmd11)
            print("\n\n")

    @snoop
    def daemon_reload(self):
        """
        Reloads the daemons of all services and timers.

        Necessary after any alteration to the *Systemd* services.

        Runs the following command::

            sudo systemctl daemon-reload
        """
        self.sbproc("sudo systemctl daemon-reload")

    @snoop
    def edit_service(self):
        """
        Stops the units, opens the service or timer in *$EDITOR*, reloads *Systemmd* daemon and restarts units.

        Requires a *unit* value.

        Runs the following commands in succession::

            sudo systemctl stop <service>
            sudo vim /usr/lib/systemd/system/<service>
            sudo systemctl daemon-reload
            sudo systemctl start <service>
        """
        for unit in self.units:
            cmd10 = f"sudo systemctl stop {unit}"
            self.sbproc(cmd10)
            cmd12 = f"sudo vim '/usr/lib/systemd/system/{unit}'"
            self.sbproc(cmd12)
            cmd13 = "sudo systemctl daemon-reload"
            self.sbproc(cmd13)
            cmd11 = f"sudo systemctl start {unit}"
            self.sbproc(cmd11)

    @snoop
    def reset_failed(self):
        """
        After deleting units, run this command to have Systemd erase them.\n
        If you don't, it will complain that it can't find the unit.

        Runs the following command::

            sudo systemctl reset-failed
        """
        self.sbproc("sudo systemctl reset-failed")

    @snoop
    def delete_service(self):
        """
        1.  Stops the service.
        2.  Disables it.
        3.  Deletes files.

        :var str decision: User input. Confirms if he wants to delete the services belonging to current *unit*.\n
            If 'yes', appends service name to list.\n
            If 'no':\n
        :var str deci: User input. Asks what *unit* he wants to delete.\n
        *deci* appends new choice to list. If no choice was made, the program exits.\n
        For each service in the list, these commands are run::

           sudo systemctl stop <service>
           sudo systemctl disable <service>
           sudo trash /usr/lib/systemd/system/<service>
           sudo systemctl daemon-reload
           sudo systemctl reset-failed
        """
        # List whre all services chosen for deletion by the user, will be housed.
        decision_lst = []

        # 'Dummy Service' is posted when doing general queries, those that didn't chose a particular
        # service at the beginning. If there are no 'dummy_service', that means there are services
        # associated with this query. We ask the user if he wants de delete them. If yes, we had the
        # services to 'decision_lst', if no, we assume the user wants to choose another service to
        # delete. We show him a list of all services and ask him to choose. This seconf option is
        # what the user would see if he came from a generalistic query.
        if "dummy_service" not in self.units:
            for unit in self.units:
                decision = input(
                    click.style(
                        f" ++ Do you want to disable unit {unit}? [y/n] ",
                        fg="bright_white",
                        bold=True,
                    )
                )
                if decision == "y":
                    decision_lst.append(f"{unit}")
        else:
            query = "SELECT DISTINCT id, name, unit_name, unit_type FROM services"
            # Calls function that does db calls to download data.
            data = self.db_getdata(query)
            print("\n")
            print(
                click.style(
                    " ++ Choose the units to delete.", fg="bright_white", bold=True
                )
            )
            for i in data:
                print(i)
                print(click.style(f"{i[0]} - {i[2]}", fg="bright_white", bold=True))
            generalist_decision = input(
                click.style(
                    " ++ Choose a number. ",
                    fg="bright_white",
                    bold=True,
                )
            )
            # If the user doesn't choose a number, we assume he gave up.
            if generalist_decision == "":
                with suppress(KeyboardInterrupt):
                    raise SystemExit
            else:
                # If there's a list of services to delete, we separate them by spaces.
                ids = generalist_decision.split(" ")
                # We look for service names, based on the id's collected.
                decision = [c for a, b, c, d in data if str(a) in ids]
                # And add them to 'decision_lst'.
                decision_lst.extend(iter(decision))

        # Initiates a series of Systemctl's commands to do during deletion of services.
        # Although there are methods in this class for most of these commands, they are
        # written to take the name of the services from 'self.units', not 'decision_lst'.
        for service in decision_lst:
            cmd15 = f"sudo systemctl stop {service}"
            cmd16 = f"sudo systemctl disable {service}"
            cmd17 = "sudo systemctl daemon-reload"
            cmd18 = f"sudo trash /usr/lib/systemd/system/{service}"
            cmd19 = "sudo systemctl reset-failed"
            for i in [cmd15, cmd16, cmd18, cmd17, cmd19]:
                self.sbproc(i)
            # Deletes service if service.
            if service.endswith("service"):
                query = f"DELETE FROM services WHERE unit_name = '{service}'"
                self.db_commit(query)
            # Deletes service if timer.
            if service.endswith("timer"):
                query = f"DELETE FROM services WHERE unit_name = '{service}'"
                self.db_commit(query)

        print(
            click.style(
                f"The service {service} was deleted.",
                fg="bright_white",
                bold=True,
            )
        )
        # Rebuilds the choices dropdown.
        make_dropdown()
        print("\n\n")

    @snoop
    def create_service(self):
        """
        Searches for files with the prefix *service* or *timer* on the
        current working directory. If it finds them, it asks if these are the files
        to be used.\n
        :var str use_choice: User choice. *Do you want to use <service>?* If yes, it runs the method, if no, it will copy a default service file to *cwd* and open it as, *<current_dir>*.service, to create a new service.
        :var str unit_making: User choice. *What unit do you want to create?* Service, Timer or both?\n
        Runs the following commands::

            sudo vim <service_name>.service
            sudo vim <service_name>.timer\n
        These files, pre-built or freshly generated, will be:\n
        1.  Copied to the services folder::

                sudo cp <service> /usr/lib/systemd/system\n
        2.  Sent the *daemon-reload* command::

                sudo systemctl daemon-reload\n
        3.  Services are startted::

                sudo systemctl start <service>\n
        4.  Their status checked, to see it they are loaded::

                sudo systemctl <service> status\n
        This new service will be added to the db and the dropdown file updated.
        """
        cwds = os.getcwd()
        services = []
        for root, dirs, files in os.walk(cwds):
            services.extend(iter(files))
        services_present = [
            i for i in services if i.endswith(".service") or i.endswith(".timer")
        ]

        chosen_units = []
        user_negs = []
        if services_present != []:
            for service in services_present:
                use_choice = input(
                    click.style(
                        f" ++ Do you want to use {service}? [y/n] ",
                        fg="bright_white",
                        bold=True,
                    )
                )
                if use_choice == "n":
                    user_negs.append("n")
                elif use_choice == "y":
                    chosen_units.append(service)

        if not services_present or user_negs != []:
            namequery = questionary.text(
                "What do you want to call your service(s)?",
                qmark="[x]",
                style=custom_style_monitor,
            ).ask()

            servicetype = questionary.checkbox(
                "What Services do You Want to Create?",
                choices=["service", "timer"],
                qmark="[x]",
                style=custom_style_monitor,
            ).ask()

            for service in servicetype:
                newservice = f"{namequery}.{service}"
                h = self.sbproc(f"/usr/bin/sudo /usr/bin/vim {newservice}")
                chosen_units.append(h)

        for h in chosen_units:
            cmd22 = f"/usr/bin/sudo /usr/bin/cp {h} '/usr/lib/systemd/system/'"
            cmd24 = f"/usr/bin/sudo /usr/bin/systemctl start {h}"
            cmd25 = f"/usr/bin/sudo /usr/bin/systemctl status {h} > {h}.txt"
            self.sbproc(cmd22)
            self.daemon_reload()
            self.sbproc(cmd24)
            self.sbproc(cmd25)
        cmd26 = f"/usr/bin/sudo /usr/bin/systemctl status {h}"
        sleep(0.30)
        if f"{h}.txt":
            with open(f"{h}.txt", "r") as f:
                data = f.readlines()
            print("\n")
            for line in data:
                x = re.search("^\s+Active: active \(running\).+\n$", line)
                w = re.search("^\s+Active: active \(waiting\).+\n$", line)
                if x or w:
                    success = input(
                        click.style(
                            f"++ {h} is active. Do you want to see its status? [y/n]: ",
                            fg="bright_white",
                            bold=True,
                        )
                    )
                    if success == "y":
                        self.sbpro(cmd26)
                else:
                    print(
                        click.style(
                            f" ++ {h} is not active. We'll open the status view for debugging.",
                            fg="bright_white",
                            bold=True,
                        )
                    )
                    sleep(0.30)
                    self.sbproc(cmd26)
                    os.remove(f"{h.txt}")
                break

            entry()
            make_dropdown()
