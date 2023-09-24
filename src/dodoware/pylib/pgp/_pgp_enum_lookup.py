from typing import Any, Dict, Type
from enum import Enum

def _check_match(enum_value:Any, attributes:Dict[str, Any]):

    for (attribute_name, attribute_value) in attributes.items():

        if not hasattr(enum_value, attribute_name):
            raise ValueError(f"invalid attribute '{attribute_name}' for enum value type '{type(enum_value).__name__}'")

        if getattr(enum_value, attribute_name) != attribute_value:
            return False

    return True

def pgp_enum_lookup(enum_class:Type[Enum], must_exist:bool=False, **attributes):
    """
    Lookup an enum value by attributes.  The input attributes must not match
    multiple enum entries.

    Args:
        enum_class (Type[Enum]):
            The enum class.
        must_exist (bool):
            If set, a match must exist.
        attributes (Dict[str, Any]):
            Attributes to match.

    Returns:
        Enum:
            The matching enum entry.
    """

    matching_entry = None

    for enum_entry in enum_class:

        enum_value = enum_entry.value

        if _check_match(enum_value, attributes):

            if matching_entry is not None:
                raise ValueError(f"multiple matches: enum_class={enum_class.__name__} attributes={attributes}")

            matching_entry = enum_entry

    if must_exist and matching_entry is None:
        raise ValueError(f"no match: enum_class={enum_class.__name__} attributes={attributes}")

    return matching_entry
