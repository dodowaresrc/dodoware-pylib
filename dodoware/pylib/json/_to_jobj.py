import collections.abc
from ipaddress import ip_address, ip_network
from typing import Any
import pydantic
from dodoware.pylib.exception import get_ex_messages

BASIC_TYPES = (str, int, float, bool)

STRINGABLE_TYPES = (ip_address.__class__, ip_network.__class__)

def to_jobj(obj:Any) -> Any:
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

    if obj is None or isinstance(obj, BASIC_TYPES):
        return obj

    if isinstance(obj, pydantic.BaseModel):
        return obj.dict()

    if isinstance(obj, (bytes, bytearray)):
        return obj.hex()

    if isinstance(obj, STRINGABLE_TYPES):
        return str(obj)

    if isinstance(obj, BaseException):
        return get_ex_messages(obj, traceback=True)

    if isinstance(obj, collections.abc.Sequence):
        return [to_jobj(x) for x in obj]

    if isinstance(obj, collections.abc.Mapping):
        return {k: to_jobj(v) for k, v in obj.items()}

    if hasattr(obj, "__dict__"):
        return {k: to_jobj(v) for k, v in obj.__dict__.items() if not k.startswith("_")}

    return repr(obj)
