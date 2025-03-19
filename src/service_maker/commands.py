import os
import subprocess
import argparse
import json
import uuid

from abc import ABC

from service_maker.arg_processor import ArgProcessor
from service_maker.file_helper import FileHelper


class Command(ABC):
    def execute(self, **kwargs) -> None:
        raise NotImplementedError("execute(self, **kwargs")


class Create(Command):
    def __init__(self, arg_np: argparse.Namespace) -> None:
        self.arg_np = arg_np
        self.arg_processor = ArgProcessor(arg_np)
        self.file_helper = FileHelper()

    def execute(self) -> str:
        """ Implements the create method """
        sections = ['Unit', 'Service', 'Install', 'Meta']
        ordered_args = {}
        for section in sections:
            ordered_args[section] = self.arg_processor.by_section(section)
        filename = self.arg_np.Name[0]
        self.file_helper.create(filename, ordered_args)

class Update(Command):
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    def execute(self) -> str:
        """ Implements the update method """
        raise NotImplementedError("Not yet implemented")

