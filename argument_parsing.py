#  Copyright 2017-2024 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""General-purpose functions related to argument parsing."""
from __future__ import annotations

from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    _ArgumentGroup,  # noqa pylint: disable=unused-import
)
from pathlib import Path
from typing import Any, Callable

from .validation import (
    validate_float,
    validate_input_directory_path,
    validate_input_directory_paths,
    validate_input_file_path,
    validate_input_file_paths,
    validate_int,
    validate_ints,
    validate_output_directory_path,
    validate_output_file_path,
    validate_str,
)


def get_optional_arguments_group(parser: ArgumentParser) -> _ArgumentGroup:
    """Get the 'optional arguments' group from an argparser.

    Arguments:
        parser: argparser from which to get group
    Returns:
        optional arguments group
    """
    action_groups = parser._action_groups  # noqa pylint: disable=protected-access
    return next(ag for ag in action_groups if ag.title == "optional arguments")


def get_required_arguments_group(parser: ArgumentParser) -> _ArgumentGroup:
    """Get or create a 'required arguments' group from an argparser.

    Arguments:
        parser: argparser from which to get group
    Returns:
        required arguments group
    """
    action_groups = parser._action_groups  # noqa pylint: disable=protected-access
    if any((required := ag).title == "required arguments" for ag in action_groups):
        return required

    # Move "optional arguments" group below "required arguments" group
    optional = action_groups.pop()
    required = parser.add_argument_group("required arguments")
    action_groups.append(optional)

    return required


def get_arg_groups_by_name(
    parser: ArgumentParser,
    *names: str,
    optional_arguments_name: str = "optional arguments",
) -> dict[str, _ArgumentGroup]:
    """Get or create one or more argument groups by name.

    Groups will be ordered by the order in which they are specified, with additional
    groups whose names were not included in names appearing after the specified groups.

    For example, if names = ("input arguments", "operation arguments",
    "output arguments"), groups by these names will be created, yielding the final order
    of ("input arguments", "operation arguments", "output arguments",
    "optional arguments").

    The default "optional arguments" group may be renamed by providing
    optional_arguments_name.

    Arguments:
        parser: argparser for which to get arg groups
        *names: names of groups to get or create
        optional_arguments_name: name of optional arguments group
    Returns:
        dict of names to argument groups
    """
    specified_groups = {}
    for name in names:
        action_groups = parser._action_groups  # noqa pylint: disable=protected-access
        for i, ag in enumerate(action_groups):
            if ag.title == name:
                specified_groups[name] = action_groups.pop(i)
                break
        else:
            parser.add_argument_group(name)
            specified_groups[name] = action_groups.pop()

    action_groups = parser._action_groups  # noqa pylint: disable=protected-access
    additional_groups = {}
    while len(action_groups) > 0:
        ag = action_groups.pop()
        if ag.title in ["options", "optional arguments"]:
            ag.title = optional_arguments_name
        if ag.title:
            additional_groups[ag.title] = ag

    action_groups.extend(specified_groups.values())
    action_groups.extend(additional_groups.values())

    return {**specified_groups, **additional_groups}


def get_validator(function: Callable, **kwargs: Any) -> Callable:
    """Wrap a function to catch and re-raise TypeErrors as ArgumentTypeErrors.

    Arguments:
        function: function to wrap
    Returns:
        wrapped function
    """

    def wrapped(value: Any) -> Any:
        try:
            return function(value, **kwargs)
        except TypeError as error:
            raise ArgumentTypeError from error

    return wrapped


def float_arg(**kwargs: Any) -> Callable[[Any], float]:
    """Validate a float argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_float
    Returns:
        value validator function
    """
    return get_validator(validate_float, **kwargs)


def input_directory_paths_arg(**kwargs: Any) -> Callable[[Any], list[Path]]:
    """Validate an input directory paths argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_input_directory_paths
    Returns:
        value validator function
    """
    return get_validator(validate_input_directory_paths, **kwargs)


def input_directory_path_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an input directory path argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_input_directory_path
    Returns:
        value validator function
    """
    return get_validator(validate_input_directory_path, **kwargs)


def input_file_path_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an input file path argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_input_file_path
    Returns:
        value validator function
    """
    return get_validator(validate_input_file_path, **kwargs)


def input_file_paths_arg(**kwargs: Any) -> Callable[[Any], list[Path]]:
    """Validate an input file paths argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_input_file_paths
    Returns:
        value validator function
    """
    return get_validator(validate_input_file_paths, **kwargs)


def int_arg(**kwargs: Any) -> Callable[[Any], int]:
    """Validate an int argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_int
    Returns:
        value validator function
    """
    return get_validator(validate_int, **kwargs)


def ints_arg(**kwargs: Any) -> Callable[[Any], int]:
    """Validate a tuple of ints argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_ints
    Returns:
        value validator function
    """
    return get_validator(validate_ints, **kwargs)


def output_directory_path_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an output directory path argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_output_directory_path
    Returns:
        value validator function
    """
    return get_validator(validate_output_directory_path, **kwargs)


def output_file_path_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an output file path argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_output_file_path
    Returns:
        value validator function
    """
    return get_validator(validate_output_file_path, **kwargs)


def str_arg(**kwargs: Any) -> Callable[[Any], str]:
    """Validate a string argument.

    Arguments:
        **kwargs: keyword arguments to pass to validate_str
    Returns:
        value validator function
    """
    return get_validator(validate_str, **kwargs)
