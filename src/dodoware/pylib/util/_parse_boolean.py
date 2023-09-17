TRUE_VALUES = ["true", "yes", "on", "1"]

FALSE_VALUES = ["false", "no", "off", "0", ""]

MAXLEN = max(len(x) for x in TRUE_VALUES + FALSE_VALUES)


def parse_boolean(string_value: str) -> bool:
    """
    Parse an input string into a boolean value.  A `ValueError` is
    raised if the input string value is invalid.  `None` or an empty
    string maps to `False`.

    Args:
        string_value (str):
            The input string value.

    Returns:
        bool:
            The output boolean value.
    """

    if string_value is None:
        return False

    if len(string_value) <= MAXLEN:

        string_value = string_value.lower()

        if string_value in TRUE_VALUES:
            return True

        if string_value in FALSE_VALUES:
            return False

    raise ValueError(f"unable to parse string into boolean: {string_value}")
