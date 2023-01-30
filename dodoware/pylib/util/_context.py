import os
import sys
from contextlib import contextmanager
from typing import Dict, List, Union

@contextmanager
def chdir_context(path) -> None:
    """
    Create a context that changes the current working folder.

    Args:
        path (str):
            A folder path.
    """

    orig = os.getcwd()

    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(orig)

@contextmanager
def path_context(
    path:Union[str, List[str]],
    replace:bool=False,
    append:bool=False
) -> None:
    """
    Create a context that modifies `sys.path`.

    Args:
        path (Union[str, List[str]]):
            Python path elements to set.  It can either be a single path element or
            a list of path elements.
        replace (bool):
            If set, replace `sys.path` instead of updating it.
        append (bool):
            If set, put path elements at the end of `sys.path`.
    """

    if isinstance(path, str):
        path = [path]

    orig = sys.path.copy()

    try:
        if replace:
            sys.path.clear()

        if append:
            for elem in path:
                sys.path.append(elem)
        else:
            for elem in reversed(path):
                sys.path.insert(0, elem)

        yield

    finally:
        sys.path.clear()
        sys.path.extend(orig)

@contextmanager
def environ_context(envars:Dict[str, str], replace:bool=False) -> None:
    """
    Create a context that modifies `os.environ`.

    Args:
        envars (Dict[str, str]):
            A dictionary of environment variables.
        replace (bool):
            If set, replace `os.environ` instead of updating it.
    """

    orig = dict(os.environ)

    try:
        if replace:
            os.environ.clear()
        os.environ.update(envars)
        yield
    finally:
        os.environ.clear()
        os.environ.update(orig)
