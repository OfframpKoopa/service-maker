import argparse


class ArgProcessor:
    """
    The processor allows operations relative to the formatting
    of the arguments namespace object.
    It is only responsible for processing the data in a way
    that is useful for writing it or checking it.
    It does not modify the data, nor makes state change in the
    main process.
    """
    def __init__(self, arg_np: argparse.Namespace) -> None:
        self.arg_np = arg_np

    def by_section(self, section: str) -> list:
        if not section:
            return
        datas = self.arg_np.datas
        args = vars(self.arg_np)
        section_lines = []
        for parameter in datas[section]:
            line = []
            if not args[parameter]:
                line.append("# ")
            line.append(parameter)
            line.append('=')
            None if not args[parameter] else line.append(''.join(args[parameter]))
            section_lines.append(''.join(line))
        return section_lines
