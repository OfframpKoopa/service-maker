import os
import subprocess
import argparse
import json
import uuid

from abc import ABC

from service_maker.file_tools import FileManager
from service_maker.unit_adapter import UnitAdapter
from service_maker.models import Directives, RawService


class Command(ABC):
    def execute(self, **kwargs) -> None:
        raise NotImplementedError("execute(self, **kwargs")


class Create(Command):

    def execute(self, unit_adapter: UnitAdapter) -> str:
        """ Implements the create method """
        metadatas = unit_adapter.get_metadatas()
        content = unit_adapter.get_raw_service()
        file_manager = FileManager(metadatas.get("Name", [""])[0])
        file_manager.writelines(content)


class Update(Command):

    def execute(self, unit_adapter: UnitAdapter) -> str:
        """ Implements the update method """
        metadatas = unit_adapter.get_metadatas()
        file_manager = FileManager(metadatas.get("Name", [""])[0])
        current_content = RawService(file_manager.read())
        converter = UnitAdapter(current_content)

        current_directives= converter.get_directives()
        new_directives = unit_adapter.get_directives()

        current_directives.update({k: v for k, v in new_directives.items() if v is not None})
        converter = UnitAdapter(current_directives)
        file_manager.writelines(converter.get_raw_service())
        file_manager.merge()

