import collections.abc
from ipaddress import ip_address, ip_network
from typing import Any
import pydantic
from dodoware.pylib.exception import get_ex_messages

BASIC_TYPES = (str, int, float, bool)

STRINGABLE_TYPES = (ip_address.__class__, ip_network.__class__)


def to_jobj(obj: Any) -> Any:  # pylint: disable=too-many-return-statements
    """
    This function transforms an input object into something that can be
    directly serialized to JSON, YAML, or other formats.  There may be
    loss of precision for some types.  Use `pydantic` or something
    similar if rigorous serialization is required.

    Args:
        obj (Any):
            Any input object.

    Returns:
        Any:
            The transformed object, or the input object if it is already
            of a type that can be directly serialized to JSON.
    """

    obj2 = None

    if obj is None or isinstance(obj, BASIC_TYPES):
        obj2 = obj

    elif isinstance(obj, pydantic.BaseModel):
        obj2 = obj.dict()

    elif isinstance(obj, (bytes, bytearray)):
        obj2 = obj.hex()

    elif isinstance(obj, STRINGABLE_TYPES):
        obj2 = str(obj)

    elif isinstance(obj, BaseException):
        obj2 = get_ex_messages(obj, traceback=True)

    elif isinstance(obj, collections.abc.Sequence):
        obj2 = [to_jobj(x) for x in obj]

    elif isinstance(obj, collections.abc.Mapping):
        obj2 = {k: to_jobj(v) for k, v in obj.items()}

    elif hasattr(obj, "__dict__"):
        obj2 = {k: to_jobj(v) for k, v in obj.__dict__.items() if not k.startswith("_")}

    else:
        obj2 = repr(obj)

    return obj2
