import argparse
import re

DICT_REGEX = re.compile("(.+?)[=:](.+)")


class DictAction(argparse.Action):
    """
    A custom action that parses arguments in `name=value` or `name:value`
    format into a dictionary.
    """

    def __call__(self, _parser, namespace, values, option_string=None):

        m = DICT_REGEX.match(values)

        if not m:
            raise ValueError(f"bad value for DictAction: {values}")

        parsed_name = m.group(1)

        parsed_value = m.group(2)

        dict_value = getattr(namespace, self.dest)

        if dict_value is None:
            setattr(namespace, self.dest, {parsed_name: parsed_value})
        elif parsed_name in dict_value:
            raise ValueError(
                f"argument '{self.dest}' has duplicate key '{parsed_name}'"
            )
        else:
            dict_value[parsed_name] = parsed_value
