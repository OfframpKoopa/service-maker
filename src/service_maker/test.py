import json

from service_maker.utils import get_arg_namespace

from service_maker.systemd_parser import (
    DirectivesConverter, 
    SectionsConverter,
    RawServiceConverter
)

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
    """
    def __init__(self, model, doc_reference: dict) -> None:
        self.doc_reference = doc_reference
        self.strategy = None
        self.sections_keys = {"Unit", "Service", "Install"}

        # Normalizing the model received
        # then
        self.sections = None
        self.directives = None
        self.raw_service = None

        if isinstance(model, RawService):
            self.directives = self._from_raw_service(model)
        if isinstance(model, Directives):
            self.directives = model
        if isinstance(model, Sections):
            self.directives = self._from_sections(model)
        if not self._populate():
            raise Exception(f"{model} could not be processed.")

    def _populate(self) -> bool:
        if not self.directives:
            return False
        
        self._populate_sections()
        self._populate_raw_service()

        populated = (
                bool(self.directives) +
                bool(self.sections) +
                bool(self.raw_service)
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
            raw_directives[line[0]] = [line[1]] if line[1] else None

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
                    "Name": self.directives.get("Name", ""),
                    "action": self.directives.get("action", "")
                }
            }
        for key in self.sections_keys:
            raw_sections[key] = {} 
            for directive in self.doc_reference.get(key, ""):
                if not directive in self.directives.keys():
                    continue
                raw_sections[key][directive] = self.directives[directive]
        self.sections = Sections(raw_sections)

    def _populate_raw_service(self) -> None:
        self.raw_service = [''] 

    def get_directives(self) -> Directives:
        return self.directives
    
    def get_sections(self) -> Sections:
        return self.sections

    def get_raw_service(self) -> RawService:
        return self.raw_service

# Process from existing file 

# Read the service file and read its content.
file_manager = FileManager("squeex")
content = file_manager.read()

raw_service = RawService(content)

raw_sections = {
        "Unit": [{"param1": "value1"}, {"param2": "value2"}],
        "Service": [{"param3": "value3"}, {"param4": "value4"}]
        }

sections = Sections(raw_sections)

with open("src/service_maker/db.json", "r") as f:
    db = json.load(f)

arg_np = get_arg_namespace(db)
raw_directives = vars(arg_np)
directives = Directives(raw_directives)

unit_adapter = UnitAdapter(directives, db)

print(unit_adapter.get_sections().get("Unit", {}))

