"""
Module that houses a class that encompasses
all the methods that'll create the answers
to the questionnaire questions.
"""

import json
import os
import re
import subprocess
import sys
from time import sleep

import click
import isort  # noqa: F401
import questionary
import snoop
from append_to_json import entry
from making_dropdown_file import make_dropdown
from questionary import Separator, Style
from snoop import pp

subprocess.run(["isort", __file__])


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

with open("/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json", "r") as f:
    servs = f.read()  # It has to be read(), not readlines(), because the latter is a list.
    info = json.loads(servs)

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
    """

    def __init__(self, drop, units):
        self.drop = drop
        self.units = units

    # @snoop
    def active_nodes(self):
        """
        How many active nodes are there now?
        """
        cmd = f"celery -A {self.drop} inspect active"
        subprocess.run(cmd, shell=True)
        print("\n\n")

    # @snoop
    def stats(self):
        """
        Returns the inspect
        stats value.
        """
        cmd1 = f"celery -A {self.drop} inspect stats"
        subprocess.run(cmd1, shell=True)
        print("\n\n")

    # @snoop
    def reports(self):
        """
        Returns inspect report value.
        """
        cmd2 = f"celery -A {self.drop} inspect report"
        subprocess.run(cmd2, shell=True)
        print("\n\n")

    # @snoop
    def events(self):
        """
        See events.
        """
        cmd3 = f"celery -A {self.drop} control events -d"
        subprocess.run(cmd3, shell=True)
        print("\n\n")

    # @snoop
    def clock(self):
        """
        Sees clock of workers.
        """
        cmd4 = f"celery -A {self.drop} inspect clock"
        subprocess.run(cmd4, shell=True)
        print("\n\n")

    # @snoop
    def scheduled(self):
        """
        See worker that are
        seconds away of
        starting a task.
        """
        cmd5 = f"celery -A {self.drop} inspect scheduled"
        subprocess.run(cmd5, shell=True)
        print("\n\n")

    # @snoop
    def timers(self):
        """
        Shows active Systemd
        timers.
        """
        cmd6 = "sudo systemctl --no-pager list-timers"
        subprocess.run(cmd6, shell=True)
        print("\n\n")

    # @snoop
    def active_services(self):
        """
        Shows active Systemd services.
        """
        cmd7 = "systemctl --no-pager --type=service"
        subprocess.run(cmd7, shell=True)
        print("\n\n")

    # @snoop
    def service_status(self):
        """
        See services status.
        """
        for unit in self.units:
            cmd8 = f"systemctl --no-pager status {unit}"
            subprocess.run(cmd8, shell=True)
            print("\n\n")

    # @snoop
    def service_logs(self):
        """
        See logs for the services.
        """
        units = [str(i) for i in self.units]
        if "dummy_service" not in self.units:
            for unit in units:
                choice = input(click.style(f"[*] - Do you want to see logs for {unit}? [y/n] ", fg="bright_green", bold=True))
                if choice == "y":
                    cmd9 = f"sudo SYSTEMD_COLORS=1 journalctl | grep {choice}"  # Without SYSTEMD_COLORS, the output is monochrome.
                    subprocess.run(cmd9, shell=True)
                    print("\n\n")
                else:
                    pass
        else:
            cmd9_1 = "sudo SYSTEMD_COLORS=1 journalctl | grep python3"
            subprocess.run(cmd9_1, shell=True)
            print("\n\n")

    # @snoop
    def stop_service(self):
        """
        Stops execution of Systemd
        services.
        """
        for unit in self.units:
            cmd10 = f"sudo systemctl stop {unit}"
            subprocess.run(cmd10, shell=True)
            print("\n\n")

    # @snoop
    def start_service(self):
        """
        Starts unit.
        """
        for unit in self.units:
            cmd11 = f"sudo systemctl start {unit}"
            subprocess.run(cmd11, shell=True)
            print("\n\n")

    # @snoop
    def daemon_reload(self):
        """
        Reloads the daemons of all services and timers.
        Necessary after any alteration to the Systemd
        units.
        """
        cmd13 = "sudo systemctl daemon-reload"
        subprocess.run(cmd13, shell=True)
        print("\n\n")

    # @snoop
    def edit_service(self):
        """
        Stops the units, opens the service or timer
        in $EDITOR, reloads Systemmd daemon and
        restarts units.
        The reason I copied the code from the other
        methods and not just called their functions from
        here, is due to the fact that each loops through
        the self.units variable. If I had called them,
        there would be a lot of unnecessary looping.
        """
        for unit in self.units:
            cmd10 = f"sudo systemctl stop {unit}"
            subprocess.run(cmd10, shell=True)
            cmd12 = f"sudo vim '/usr/lib/systemd/system/{unit}'"
            subprocess.run(cmd12, shell=True)
            cmd13 = "sudo systemctl daemon-reload"
            subprocess.run(cmd13, shell=True)
            cmd11 = f"sudo systemctl start {unit}"
            subprocess.run(cmd11, shell=True)

    # @snoop
    def reset_failed(self):
        """
        After deleting units, run this command
        to have Systemd erase them. If you
        don't, it will complain that it can't find
        the unit.
        """
        cmd14 = "sudo systemctl reset-failed"
        subprocess.run(cmd14, shell=True)
        print("\n\n")

    # @snoop
    def delete_service(self):
        """
        First stops the unit, then disables it and
        lastly, deletes files. If service is
        completely erased, it'll delete also the
        entry on the json file and run again the
        dropdown creation file.
        The reason I repeated the 'stop_service'
        and 'daemon_reload' methods, instead of
        simply calling them from this method, is
        that if I did that, there would be a lot
        of spurious empty and dotted lines. This
        way the presentation is cleaner.
        """
        decision_lst = []

        if "dummy_service" not in self.units:
            for unit in self.units:
                decision = input(click.style(f" ++ Do you want to disable unit {unit}? [y/n] ", fg="bright_white", bold=True))
                if decision == "y":
                    decision_lst.append(f"{unit}")
        else:
            deci = input(click.style(" ++ What unit(s) do you want to delete? ", fg="bright_white", bold=True))
            if deci == "":
                sys.exit()
            else:
                decision = deci.split(" ")
            for i in decision:
                decision_lst.append(i)

        for service in decision_lst:
            cmd15 = f"sudo systemctl stop {service}"
            subprocess.run(cmd15, shell=True)
            cmd16 = f"sudo systemctl disable {service}"
            subprocess.run(cmd16, shell=True)
            cmd18 = f"sudo rm /usr/lib/systemd/system/{service}"
            subprocess.run(cmd18, shell=True)
            cmd17 = "sudo systemctl daemon-reload"
            subprocess.run(cmd17, shell=True)
            cmd19 = "sudo systemctl reset-failed"
            subprocess.run(cmd19, shell=True)

        monitor = "/home/mic/python/service_monitoring/service_monitoring"
        data = json.load(open(f"{monitor}/dropdown_info.json"))

        for i in range(len(data["dropinfo"])):
            if decision_lst == data["dropinfo"][i]["units"]:
                data["dropinfo"].pop(i)
            open(f"{monitor}/dropdown_info1.json", "w").write(json.dumps(data, indent=4, sort_keys=True))
            os.remove(f"{monitor}/dropdown_info.json")
            os.rename(f"{monitor}/dropdown_info1.json", f"{monitor}/dropdown_info.json")
            make_dropdown()

        tst = [v.get("units") for v in data["dropinfo"]]
        if decision_lst not in tst:
            for u in decision_lst:
                for t in range(len(data["dropinfo"])):
                    if u in data["dropinfo"][t]["units"]:
                        data["dropinfo"][t]["units"].remove(u)
                    open(f"{monitor}/dropdown_info1.json", "w").write(json.dumps(data, indent=4, sort_keys=True))
                    os.remove(f"{monitor}/dropdown_info.json")
                    os.rename(f"{monitor}/dropdown_info1.json", f"{monitor}/dropdown_info.json")
                    make_dropdown()

        print("\n\n")

    # @snoop
    def create_service(self):
        """
        It will first search for files with the prefix 'service' or 'timer' on the
        current working directory. If it finds them, it asks if these are the files
        to be used, if yes, it processes them with the program, if no, it will copy a
        default service file to cwd and open it as file called, '<current_dir>.service'.
        Then it will ask if you want to create a timer, if yes, it's same procedure
        as it was for service, but now we use a default timer file.
        These files, pre-built or made now, will be copied to '/usr/lib/systemd/system',
        send the daemon-reload' command, their status checked, to see it they are loaded,
        started with systemctl and checked again, to see if they are working correctly.
        This new service will be manually added to the json file and the dropdown file updated.
        """
        cwds = os.getcwd()
        services = []
        for root, dirs, files in os.walk(cwds):
            for file in files:
                services.append(file)
        services_present = [i for i in services if i.endswith(".service") or i.endswith(".timer")]

        chosen_units = []
        user_negs = []
        if services_present != []:
            for service in services_present:
                use_choice = input(click.style(f" ++ Do you want to use {service}? [y/n] ", fg="bright_white", bold=True))
                if use_choice == "y":
                    chosen_units.append(service)
                if use_choice == "n":
                    user_negs.append("n")
        if services_present == [] or user_negs != []:
            unit_making = questionary.select(
                "What units do you want to create?",
                qmark="[x]",
                pointer="++",
                use_indicator=True,
                style=custom_style_monitor,
                choices=["Service", "Timer", "Both", "None", "Exit"],
            ).ask()
            tail = os.path.basename(os.path.normpath(cwds))
            cmd20 = f"sudo /usr/bin/vim {tail}.service"
            cmd21 = f"sudo /usr/bin/vim {tail}.timer"
            if unit_making == "None":
                pass
            if unit_making == "Exit":
                sys.exit()
            if unit_making == "Service":
                subprocess.run(cmd20, cwd=cwds, shell=True)
                chosen_units.append(f"{tail}.service")
            if unit_making == "Timer":
                subprocess.run(cmd21, cwd=cwds, shell=True)
                chosen_units.append(f"{tail}.timer")
            if unit_making == "Both":
                subprocess.run(cmd20, cwd=cwds, shell=True)
                subprocess.run(cmd21, cwd=cwds, shell=True)
                chosen_units.append(f"{tail}.service")
                chosen_units.append(f"{tail}.timer")

        for h in chosen_units:
            cmd22 = f"/usr/bin/sudo /usr/bin/cp {h} '/usr/lib/systemd/system/'"
            subprocess.run(cmd22, cwd=cwds, shell=True)
            cmd23 = "/usr/bin/sudo /usr/bin/systemctl daemon-reload"
            subprocess.run(cmd23, shell=True)
            cmd24 = f"/usr/bin/sudo /usr/bin/systemctl start {h}"
            subprocess.run(cmd24, shell=True)
            cmd25 = f"/usr/bin/sudo /usr/bin/systemctl status {h} > {h}.txt"
            subprocess.run(cmd25, shell=True)

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
                    success = input(click.style(f"++ {h} is active. Do you want to see its status? [y/n]: ", fg="bright_white", bold=True))
                    if success == "y":
                        subprocess.run(cmd26, shell=True)
                    break
                else:
                    print(click.style(f" ++ {h} is not active. We'll open the status view for debugging.", fg="bright_white", bold=True))
                    sleep(0.30)
                    subprocess.run(cmd26, shell=True)
                    break
        entry()
        make_dropdown()
