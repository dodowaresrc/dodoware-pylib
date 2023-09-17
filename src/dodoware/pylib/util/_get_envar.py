from typing import Union
import os
from dodoware.pylib.util._parse_boolean import parse_boolean


def get_envar(
    name: str,
    default: Union[str, int, bool] = None,
    required: bool = False,
    as_int: bool = False,
    as_bool: bool = False,
) -> Union[str, int, bool]:

    """
    Get an environment variable.

    Args:
        name (str):
            The environment variable name.  Must not be `None` or an empty string.
        default (Union[str, int, bool]):
            The default value to return if the environment variable is not set.
            If a default value is provided, it should be of a type consistent with
            the `as_int` and `as_bool` inputs but that is not enforced.
        required (bool):
            Controls what happens if the environment variable is not set and no
            default value is provided.  For `required=False`, return `None`.
            For `required=True`, raise `ValueError`.
        as_int (bool):
            If set, convert the environment variable value to an integer.
        as_bool (bool):
            If set, convert the environment variable value to a boolean.
            This setting is ignored if `as_int` is also set.

    Returns:
        The environment variable value as a `str`, `int`, or `bool` depending
        on the input flags.
    """

    if not name:
        raise ValueError("environment variable name must be set")

    value = os.getenv(name)

    if value is None:
        if default is not None:
            return default
        if required:
            raise ValueError(f"environment variable not set: {name}")
        return None

    if as_int:
        try:
            return int(value)
        except ValueError as ex:
            raise ValueError(f"integer conversion failed for envar: {name}") from ex

    if as_bool:
        try:
            return parse_boolean(value)
        except ValueError as ex:
            raise ValueError(f"boolean conversion failed for envar: {name}") from ex

    return value
