import json

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
    
    - doc_reference is a dict with sections as key and 
    a list of all their possible parameters as value.
    - model is a model from models.py

    The adapter works by converting every types inputed as
    a Directives type. Because it's the easiest to work with
    and transform to other types.

    The sections, directives and raw_service attributes are
    populated automatically at initialization.
    
    The "populate" method are internal because they need to
    be called in the current order for the class to function.
    
    Implementing the UnitAdapter should not required any
    other steps than initializing it.

    """
    def __init__(self, model) -> None:
        self.doc_reference = DocReference()
        self.sections_keys = ["Unit", "Service", "Install"]

        self._sections = None
        self._directives = None
        self._raw_service = None

        if isinstance(model, RawService):
            self._directives = self._from_raw_service(model)
        if isinstance(model, Directives):
            self._directives = model
        if isinstance(model, Sections):
            self._directives = self._from_sections(model)
        if not self._populate():
            raise Exception(f"{model} could not be processed.")

    def _populate(self) -> bool:
        if not self._directives:
            return False
        
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
                    "Name": self._directives.get("Name", ""),
                    "action": self._directives.get("action", "")
                }
            }
        for key in self.sections_keys:
            print(key)
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
        return self.get_sections()["Meta"]

