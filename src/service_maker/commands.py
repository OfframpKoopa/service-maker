import os
import subprocess
import argparse
import json
import uuid

from abc import ABC

from service_maker.file_tools import FileManager
from service_maker.unit_adapter import UnitAdapter
from service_maker.models import Directives


class Command(ABC):
    def execute(self, **kwargs) -> None:
        raise NotImplementedError("execute(self, **kwargs")


class Create(Command):

    def execute(self, unit_adapter: UnitAdapter) -> str:
        """ Implements the create method """
        metadatas = unit_adapter.get_sections()["Meta"]
        content = unit_adapter.get_raw_service()
        file_manager = FileManager(metadatas["Name"][0])
        file_manager.writelines(content)

class Update(Command):

    def execute(self, unit_adapter: UnitAdapter) -> str:
        """ Implements the update method """
        raise NotImplementedError("Update command is not yet implemented")
