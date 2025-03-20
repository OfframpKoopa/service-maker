import os
import subprocess
import argparse
import json
import uuid

from abc import ABC

from service_maker.file_helper import FileManager
from service_maker.arg_processor import by_section


class Command(ABC):
    def execute(self, **kwargs) -> None:
        raise NotImplementedError("execute(self, **kwargs")


class Create(Command):
    def __init__(self, arg_np: argparse.Namespace) -> None:
        self.arg_np = arg_np

    def execute(self) -> str:
        """ Implements the create method """
        sections = getattr(self.arg_np, "datas", {}).keys()
        ordered_args = {}

        # Parse and organize the directives in the ordered_args dict.
        for section in sections:
            ordered_args[section] = by_section(self.arg_np, section)

        # Operate os level file creation.
        name = getattr(self.arg_np, "Name", [""])[0]
        file_manager = FileManager(name)
        file_manager.create_tmp()
        for section in sections:
            if section == "Meta":
                continue
            file_manager.write(f"[{section}]")
            for directive in ordered_args.get(section, []):
                file_manager.write(directive)

        file_manager.merge()


class Update(Command):
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    def execute(self) -> str:
        """ Implements the update method """
        raise NotImplementedError("Not yet implemented")

