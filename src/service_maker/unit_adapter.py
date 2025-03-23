import json
from types import SimpleNamespace

from service_maker.utils import get_arg_namespace
from service_maker.doc_reference import DocReference

from service_maker.models import (
    Directives,
    Sections,
    RawService
)

from service_maker.file_tools import FileManager


class UnitAdapter:
    """
    Takes one data type from models.py and can return
    its content as an instance of any other data type.

    This object is a representation of the state of the
    model passed at initialisation.

    If the state of the model is changed, the update(model)
    method will update the current adapter instance with
    the new model.
        -> This is mainly done for semantic purpose, as it allows
            to not instanciate a new adapter each time the data of 
            a service is changed in the implementation.

    Examples

        # 1. Editing the smartd service

            smartd = UnitAdapter(Directives(data))

            raw_smartd = smartd.get_raw_service()
            raw_smartd.append("# This is the last line of the service file")
        
            smartd.update(raw_smartd)
    """
    def __init__(self, model) -> None:
        """
        model : A data type from models.py.

        The adapter works by converting every types inputed as
        a Directives type, then populates the other type with it.

        The sections, directives and raw_service attributes are
        populated automatically at initialization.
    
        The "populate" methods are internal because they need to
        be called in a specific order for the class to function.

        """
        self.doc_reference = DocReference()
        self.sections_keys = ["Unit", "Service", "Install"]
        self._populate(model)

    def _populate(self, model) -> bool:

        self._sections = None
        self._directives = None
        self._raw_service = None

        if isinstance(model, RawService):
            self._directives = self._from_raw_service(model)
        if isinstance(model, Directives):
            self._directives = model
        if isinstance(model, Sections):
            self._directives = self._from_sections(model)

        self._populate_sections()
        self._populate_raw_service()

        populated = (
                bool(self._directives) +
                bool(self._sections) +
                bool(self._raw_service)
            )
        return populated == 3

    def _from_raw_service(self, raw_service: RawService) -> Directives:
        """
        raw_service is a data type which inherit from the list type,
        and is immutable.

        A Directives type is a dictionary which has all parameters in
        the service file as keys, and their current values as parameters.

        To go from RawService to Directives, we need to parse the lines
        from the file: 
            - ignore the section mentions
            - delete the # that may be at the beginning of the line
            - strip the trailing "\n"
            - split by "=" and add the index 0 as key and 1 as value
        """
        raw_directives = {}
        for raw_line in raw_service:
            if raw_line.startswith("["):
                continue
            line = raw_line
            line = line.strip("# ")
            line = line.strip("\n")
            line = line.split("=")
            raw_directives[line[0]] = [line[1]] if len(line) > 1 else None

        return Directives(raw_directives)

    def _from_sections(self, sections: Sections) -> Directives:
        """
        sections is a data type which inherit from dict,
        and is immutable.

        A Sections type is a dictionnary in which the keys
        are the section names (Unit, Service, Install), and
        as values they have a list of dictionnary that are the
        parameters and their values.

        To get Directives from a Sections object, we need to
        extract all parameter/value pairs in the list inside
        the sections key and add them to a Directives dictionnary.
        """
        raw_directives = {}

        for section, directives in sections.items():
            for directive in directives:
                for param, value in directive.items():
                    raw_directives[param] = [value] if value else None
        return Directives(raw_directives)

    def _populate_sections(self) -> None:
        raw_sections = {
                "Meta": {
                    "name": self._directives.get("name", ""),
                    "action": self._directives.get("action", "")
                }
            }
        for key in self.sections_keys:
            raw_sections[key] = {} 
            for directive in self.doc_reference.get(key, ""):
                if not directive in self._directives.keys():
                    continue
                raw_sections[key][directive] = self._directives[directive]
        self._sections = Sections(raw_sections)

    def _populate_raw_service(self) -> None:
        """ raw service is a list of lines basically ready to
        be written in the service file.
        - Sections appear as "[Name]\n"
        - Directives lines: param=value\n
        - If the value is None, "# " prefixes the line
        
        This method needs to be called AFTER self._sections is 
        populated.
        """
        def parsed_dir_line(param: str, value: str) -> str:
            line = ""
            if not value:
                line += "# "
                value = ""
            line += param
            line += "="
            line += value
            line += "\n"
            return line

        if not self.get_sections():
            raise Exception("Tried to populate raw_service before sections.")
        
        raw_service = [] 
        sections = self.get_sections()
        raw_service.append("# This file has been generated with service-maker\n")
        for section, directives in sections.items():
            if section == "Meta":
                continue
            sec_nm = "\n[" + section + "]\n"
            raw_service.append(sec_nm)
            for param, values in directives.items():
                if values is None:
                    line = parsed_dir_line(param, None)
                elif len(values) > 1:
                    for val in values:
                        line = parsed_dir_line(param, val)
                        raw_service.append(line)
                    continue
                elif len(values) == 1:
                    line = parsed_dir_line(param, values[0])

                raw_service.append(line)

        self._raw_service = RawService(raw_service)

    def get_directives(self) -> Directives:
        return self._directives
    
    def get_sections(self) -> Sections:
        return self._sections

    def get_raw_service(self) -> RawService:
        return self._raw_service
    
    def get_metadatas(self) -> dict:
        metadatas = self.get_sections()["Meta"]
        parsed_metadatas = {key: value[0] for key, value in metadatas.items()} 
        metadatas_np = SimpleNamespace(**parsed_metadatas)
        return metadatas_np

    def update(self, model):
        self._populate(model)

