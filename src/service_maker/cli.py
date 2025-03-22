
import service_maker.command_invoker as command_invoker

from service_maker.utils import get_arg_namespace, get_doc_reference_data
from service_maker.doc_reference import DocReference
from service_maker.unit_adapter import UnitAdapter
from service_maker.models import Directives


def main() -> None:
    """ Entry point for command line calls. 
 
    Creates an argparse.Namespace which 
    contains the arguments sent through
    the command line by the user.
    
    Any dict can be normalized as a Directives
    object (a custom data type that is found in 
    models.py)

    With a Directives object successfully 
    instanciated, it can be passed to a 
    UnitAdapter object with a DocReference 
    (see DocReference docstring) object.
    The UnitAdapter will allow any Commands
    class to perform any kind of operations.
    """

    doc_reference = DocReference()

    arg_np = get_arg_namespace(doc_reference)
    directives = Directives(vars(arg_np))

    unit_adapter = UnitAdapter(directives)
    action = directives.get("action", [""])[0]
    command = command_invoker.get_command(action)
    command.execute(unit_adapter)

#    try:
#        command.execute()
#        print(f"{command.arg_np.Name} successfully created/updated.")
#    except Exception as e:
#        print(f"[error] ServiceMaker encountered following issue: {e}")


if __name__ == '__main__':
    main()
