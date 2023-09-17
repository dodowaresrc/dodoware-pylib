from argparse import RawTextHelpFormatter
from dodoware.pylib.util import get_envar


class HelpFormatter(RawTextHelpFormatter):
    """
    An `argparse` help formatter that provides some control over
    help formatting.  This is particularly useful for test cases
    where the console width can be inconsistent.
    """

    def __init__(self, *args, **kwargs):

        kwargs["width"] = get_envar(
            "DODOWARE_HELP_FORMATTER_WIDTH", as_int=True, default=100
        )

        kwargs["max_help_position"] = get_envar(
            "DODOWARE_HELP_FORMATTER_MAX", as_int=True, default=32
        )

        super().__init__(*args, **kwargs)
