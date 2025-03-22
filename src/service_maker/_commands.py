import os
import subprocess
import argparse
import json
import uuid

from abc import ABC

from service_maker.file_tools import FileManager
from service_maker.arg_processor import by_section, by_raw_list, update_ordered_args 


class Command(ABC):
    def execute(self, **kwargs) -> None:
        raise NotImplementedError("execute(self, **kwargs")


class Create(Command):

    def execute(self, arg_np: argparse.Namespace) -> str:
        """ Implements the create method """
        sections = getattr(arg_np, "datas", {}).keys()
        ordered_args = {}

        # Parse and organize the directives in the ordered_args dict.
        for section in sections:
            ordered_args[section] = by_section(arg_np, section)
        
        # Build the final list with the raw lines
        raw_lines = []
        for section in sections:
            if section == "Meta":
                continue
            raw_lines.append(f"[{section}]")
            for directive in ordered_args.get(section, []):
                raw_lines.append(directive)

        # Operate os level file creation.
        name = getattr(arg_np, "Name", [""])[0]
        file_manager = FileManager(name)
        file_manager.create_tmp()
        file_manager.writelines(raw_lines)
        file_manager.merge()


class Update(Command):

    def execute(self, arg_np: argparse.Namespace) -> str:
        """ Implements the update method """
        name = getattr(arg_np, "Name", [""])[0]
        sections = getattr(arg_np, "datas", {}).keys()
        file_manager = FileManager(name)
        raw_content = file_manager.read()
        current_ordered_args = by_raw_list(raw_content)
        new_args = vars(arg_np)
        updated_args = update_ordered_args(current_ordered_args, new_args)

        # Create ordered_args
        for section in sections:
            ordered_args[section] = by_section(arg_np, section)
        file_manager.create_tmp()

