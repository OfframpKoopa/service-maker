
from abc import ABC, abstractmethod

from service_maker.file_tools import FileManager
from service_maker.unit_adapter import UnitAdapter
from service_maker.models import Directives, RawService


class Command(ABC):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._name = cls.__name__.lower()

    @classmethod
    def get_name(cls) -> str:
        return cls._name
    
    @abstractmethod
    def execute(self, **kwargs) -> None:
        pass


class Create(Command):

    def execute(self, service: UnitAdapter) -> str:
        """ Implements the create method """
        metadatas = service.get_metadatas()
        content = service.get_raw_service()
        file_manager = FileManager(metadatas.name)
        file_manager.writelines(content)


class Update(Command):

    def execute(self, new_service: UnitAdapter) -> str:
        """ Implements the update method """
        metadatas = new_service.get_metadatas()
        file_manager = FileManager(metadatas.name)
        raw_file = file_manager.read()

        current_service = UnitAdapter(RawService(raw_file))
        current_directives = current_service.get_directives()
        new_directives = new_service.get_directives()

        current_directives.update({k: v for k, v in new_directives.items() if v is not None})

        new_service.update(current_directives)
        file_manager.writelines(new_service.get_raw_service())
        file_manager.commit()

