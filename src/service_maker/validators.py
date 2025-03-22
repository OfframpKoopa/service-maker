class Validators:
    """ 
    This class serves as a namespace for the model validators.
    You can use it this way : 
        validators = Validators()
        validators.directives.key 
            -> Returns the key validators for directives
    """
    class directives:
        
        @staticmethod
        def key(inst, attr, key):
            """ directives should only have str keys. """
            if not isinstance(key, str):
                raise ValueError(f"{key} is not a valid key for a Directives object")

        @staticmethod
        def value(inst, attr, value):
            """ directives value should be none or a list """
            if value is not None and not isinstance(value, list):
                raise ValueError(f"{value} is not a valid value for a Directives object")

    class sections:

        @staticmethod
        def key(inst, attr, key):
            pass

        @staticmethod
        def value(inst, attr, value):
            pass

    class raw_service:

        @staticmethod
        def key(inst, attr, key):
            pass

        @staticmethod
        def value(inst, attr, value):
            pass

