"""Module deletes services from the json file."""
import json
import os

import click
import snoop

from making_dropdown_file import make_dropdown


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


def choose_app():
    """Asks the user what service he wants to delete."""
    choice = input(click.style("What is the service you want to delete? ", fg="bright_white", bold=True))

    return choice


# @logger.catch
# @snoop
def delete_json():
    """
    Gets service name to delete from last function,
    creates new json object through a dictionary
    comprehension that excludes the chosen service,
    creates a new json updated json file, deletes the
    old one, renames the new file with the
    name of the old one and calls the 'make_dropdown'
    function, to update the app dropdown.
    """

    select = choose_app()

    with open("/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json", "r+") as f:
        data = json.load(f)
        ndata = [i for i in data["dropinfo"] if i["name"] != select]

    with open("/home/mic/python/service_monitoring/service_monitoring/dropdown_info1.json", "w") as f:
        f.seek(0)
        json.dump(ndata, f, indent=4)

    os.remove("/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json")
    os.rename("/home/mic/python/service_monitoring/service_monitoring/dropdown_info1.json", "/home/mic/python/service_monitoring/service_monitoring/dropdown_info.json")
    make_dropdown()

    print(click.style(f"Service with name {select} was deleted.", fg="bright_white", bold=True))


if __name__ == "__main__":
    delete_json()
