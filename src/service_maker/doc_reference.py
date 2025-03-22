import os
import json

class DocReference(dict):
    """
    Data type class meant to handle the doc reference object
    with stronger typing, validation and immutability than 
    passing a dict around.

    Auto-fills with the doc_reference.json file.
    """
    def __init__(self) -> None:
        base_path = os.path.dirname(__file__)
        doc_ref_file = os.path.join(base_path, "doc_reference.json")
        with open(doc_ref_file, "r") as f:
            data = json.load(f)

        super().__init__(data)
        for k, v in data.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        return getattr(self, key)
                
    def __repr__(self):
        return repr(vars(self))

    def __str__(self):
        return str(vars(self))

