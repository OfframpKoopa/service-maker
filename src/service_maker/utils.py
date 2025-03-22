import json
import os
import argparse

from service_maker.doc_reference import DocReference

CMDS = ["create", "update"]


def get_arg_namespace(doc_reference: DocReference) -> argparse.Namespace:
    """
    Returns a argparse namespace object from the passed 
    json file.
    Every argument is added as a list, even if they 
    can technically be added only once.
    """
    arg_parser = argparse.ArgumentParser()
    for section, params in doc_reference.items():
        for param in params:
            arg_parser.add_argument("--" + param, action="append")
    arg_parser.add_argument("action", choices=CMDS, action="append")
    return arg_parser.parse_args()


def get_doc_reference_data(filename: str = "doc_reference.json") -> dict:
    """ returns the doc_reference json as a dict.  """
    base_path = os.path.dirname(__file__)
    doc_reference_path = os.path.join(base_path, filename)
    with open(doc_reference_path, "r") as f:
        return json.load(f)

