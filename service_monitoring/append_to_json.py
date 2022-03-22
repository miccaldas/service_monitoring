"""Module Docstring"""
import json
import subprocess

import isort  # noqa: F401
import snoop
from loguru import logger

fmt = "{time} - {name} - {level} - {message}"
logger.add("../logs/info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
logger.add("../logs/error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)  # noqa: E501

subprocess.run(["isort", __file__])


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@logger.catch
@snoop
def test():
    """"""

    entry = {"app": "none", "name": "service_monitoring", "path": "none", "units": ["service_monitoring.service"]}

    with open("dropdown_info.json", "r+") as f:
        data = json.load(f)
        data["dropinfo"].append(entry)
        f.seek(0)
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    test()
