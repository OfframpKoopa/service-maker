
class DocReference(dict):
    """
    Data type class meant to handle the doc reference object
    with stronger typing, validation and immutability than 
    passing a dict around.
    """
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        for k, v in data.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        return getattr(self, key)
                
    def __repr__(self):
        return repr(vars(self))

    def __str__(self):
        return str(vars(self))

