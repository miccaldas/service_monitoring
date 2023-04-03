"""
Module Docstring
"""
import snoop
from snoop import pp

# from configs.config import Efs, tput_config
# import os
# import subprocess
from dotenv import load_dotenv


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


@snoop
def test():
    """"""
    print("caralho")


if __name__ == "__main__":
    test()
