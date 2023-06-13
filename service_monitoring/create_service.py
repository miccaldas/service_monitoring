"""
Creates new Systemd service and registers it on the db.
"""
import os
import pickle
import re
import subprocess

import snoop
from mysql.connector import Error, connect
from rich import text
from rich.console import Console

from service_monitoring.make_dropdown import make_dropdown

# from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])
console = Console(width=260)


@snoop
def create_service_files():
    """
    Creates the files for the service. You can have them pre-written, it'll
    detect it and use them as base. If not, it'll ask you some questions and
    ask you to work on a template for services and timers.
    """
    cwd = os.getcwd()
    files = os.listdir(cwd)
    units = [i for i in files if i.endswith(".service") or i.endswith(".timer")]
    service_files = []

    # In case you already have the service's files.
    if units != []:
        for unit in units:
            prefile = console.input(
                f"[bold #E2C275]  <X> - Do you want to use the {unit} file?[y/n] "
            )
            if "y":
                # We create a tuple with the identifiers 'service/timer'
                if unit.endswith("service"):
                    service_files.append(("service", f"{unit}"))
                if unit.endswith("timer"):
                    service_files.append(("timer", f"{unit}"))

    title = console.input("[bold #E2C275]   <X> - What is the title of your units? ")

    # In case you haven't.
    if service_files == []:
        newfiles = console.input(
            "[bold #E2C275]  <X> - Will you need:\n  [1] - To write a service only,\n  [2] - To write a timer only,\n  [3] - To write both.\n  Choose a number: "
        )
        if newfiles == "1":
            cmd = f"/usr/bin/sudo /usr/bin/vim {title}.service"
            subprocess.run(cmd, shell=True)
            service_files.append(f"{title}.service")
        if newfiles == "2":
            cmd = f"/usr/bin/sudo /usr/bin/vim {title}.timer"
            subprocess.run(cmd, shell=True)
            service_files.append(f"{title}.timer")
        if newfiles == "3":
            cmd = f"/usr/bin/sudo /usr/bin/vim {title}.timer {title}.service"
            subprocess.run(cmd, shell=True)
            service_files.append(("service", f"{title}.service"))
            service_files.append(("timer", f"{title}.timer"))

    # The title is appended to make it easier to register on the database.
    service_files.append(title)

    with open("service_files.bin", "wb") as f:
        pickle.dump(service_files, f)


# @snoop
def systemctl_deployment():
    """
    We put the files in the correct location,
    enable them, start them and see their status.
    """
    with open("service_files.bin", "rb") as f:
        service_files = pickle.load(f)

    # The last entry in 'service_files' is the title, not services.
    services = [service_files[0][1], service_files[1][1]]

    # Usual systemd initiation's rituals.
    for h in services:
        copy = f"/usr/bin/sudo /usr/bin/cp {h} '/usr/lib/systemd/system/'"
        subprocess.run(copy, shell=True)
        reload = "/usr/bin/sudo /usr/bin/systemctl daemon-reload"
        subprocess.run(reload, shell=True)
        enable = f"/usr/bin/sudo /usr/bin/systemctl enable {h}"
        subprocess.run(enable, shell=True)
        start = f"/usr/bin/sudo /usr/bin/systemctl start {h}"
        subprocess.run(start, shell=True)
        status_file = f"/usr/bin/sudo /usr/bin/systemctl status {h} > {h}.txt"
        subprocess.run(status_file, shell=True)
        status = f"/usr/bin/sudo /usr/bin/systemctl status {h}"

    # We check to see if the service was correctly created.
    if f"{h}.txt":
        with open(f"{h}.txt", "r") as f:
            data = f.readlines()
        print("\n")
        # This is some regex to check for the existence of some text that only shows
        # when the service creation was successful and it is active.
        for line in data:
            x = re.search("^\s+Active: active \(running\).+\n$", line)
            w = re.search("^\s+Active: active \(waiting\).+\n$", line)
            if x or w:
                success = console.input(
                    f"[bold #E2C275]  <X> - {h} is active. Do you want to see it's status?[y/n] "
                )
                if success == "y":
                    subprocess.run(status, shell=True)
            else:
                console.print(
                    f"[bold #E2C275]  <X> - {h} is not active. We'll oopen it's status for debugging"
                )
                subprocess.run(status, shell=True)


# @snoop
def db_input():
    """
    Let's register this new service on the database.
    #"""
    with open("service_files.bin", "rb") as f:
        sf = pickle.load(f)

    answers = []
    if sf != []:
        for i in sf:
            if i[0] == "service":
                rowservice = (f"{sf[2]}", f"{i[1]}", "service")
                answers.append(rowservice)
            if i[0] == "timer":
                rowtimer = (f"{sf[2]}", f"{i[1]}", "timer")
                answers.append(rowtimer)

    try:
        conn = connect(
            host="localhost", user="mic", password="xxxx", database="services"
        )
        cur = conn.cursor()
        for answer in answers:
            query = f"INSERT INTO services (name, unit_name, unit_type) VALUES{answer}"
            cur.execute(query)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    # Module that recreates the dropdown with the app's available services.
    make_dropdown()


# @snoop
def maincreate():
    """
    Calls all other functions.
    """
    create_service_files()
    systemctl_deployment()
    db_input()


if __name__ == "__main__":
    maincreate()
