import json
import os
import argparse

from service_maker.doc_reference import DocReference

CMDS = ["create", "update"]


def get_arg_namespace() -> argparse.Namespace:
    """
    Returns a argparse namespace object 
    Every argument is added as a list, even if they 
    can technically be added only once.
    """
    doc_reference = DocReference()
    arg_parser = argparse.ArgumentParser()
    for section, params in doc_reference.items():
        for param in params:
            if param == "name":
                arg_parser.add_argument("--" + param, action="append", required=True)
                continue
            if param == "action":
                arg_parser.add_argument("action", choices=CMDS, action="append")
                continue
            arg_parser.add_argument("--" + param, action="append")
    return arg_parser.parse_args()


