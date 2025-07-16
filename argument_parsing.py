#  Copyright 2017-2025 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""General-purpose functions related to argument parsing."""

from __future__ import annotations

from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    _ArgumentGroup,  # noqa pylint
)
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .validation import (
    validate_float,
    validate_input_directories,
    validate_input_directory,
    validate_input_file,
    validate_input_files,
    validate_int,
    validate_ints,
    validate_output_directory,
    validate_output_file,
    validate_str,
)


def get_optional_arguments_group(parser: ArgumentParser) -> _ArgumentGroup:
    """Get the 'optional arguments' group from an argparser.

    Arguments:
        parser: Argparser to get group from
    Returns:
        Optional arguments group
    """
    action_groups = parser._action_groups  # noqa pylint: disable=protected-access
    return next(ag for ag in action_groups if ag.title == "optional arguments")


def get_required_arguments_group(parser: ArgumentParser) -> _ArgumentGroup:
    """Get or create a 'required arguments' group from an argparser.

    Arguments:
        parser: Argparser to get group from
    Returns:
        Required arguments group
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
        parser: Argparser to get groups from
        *names: Names of groups to get or create
        optional_arguments_name: Name of optional arguments group
    Returns:
        Dictionary of names to argument groups
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
    """Get a function that can be called with the same signature as function.

    Arguments:
        function: Function to be wrapped
        **kwargs: Keyword arguments to pass to wrapped function
    Returns:
        Wrapped function
    """

    def wrapped(value: Any) -> Any:
        """Wrapped function.

        Arguments:
            value: Value to be validated
        Returns:
            Validated value
        Raises:
            ArgumentTypeError: If TypeError is raised by wrapped function
        """
        try:
            return function(value, **kwargs)
        except TypeError as error:
            raise ArgumentTypeError from error

    return wrapped


def float_arg(**kwargs: Any) -> Callable[[Any], float]:
    """Validate a float argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_float
    Returns:
        Value validator function
    """
    return get_validator(validate_float, **kwargs)


def input_directories_arg(**kwargs: Any) -> Callable[[Any], list[Path]]:
    """Validate an input directory paths argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_input_directories
    Returns:
        Value validator function
    """
    return get_validator(validate_input_directories, **kwargs)


def input_directory_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an input directory path argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_input_directory
    Returns:
        Value validator function
    """
    return get_validator(validate_input_directory, **kwargs)


def input_file_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an input file path argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_input_file
    Returns:
        Value validator function
    """
    return get_validator(validate_input_file, **kwargs)


def input_files_arg(**kwargs: Any) -> Callable[[Any], list[Path]]:
    """Validate an input file paths argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_input_files
    Returns:
        Value validator function
    """
    return get_validator(validate_input_files, **kwargs)


def int_arg(**kwargs: Any) -> Callable[[Any], int]:
    """Validate an int argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_int
    Returns:
        Value validator function
    """
    return get_validator(validate_int, **kwargs)


def ints_arg(**kwargs: Any) -> Callable[[Any], int]:
    """Validate a tuple of ints argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_ints
    Returns:
        Value validator function
    """
    return get_validator(validate_ints, **kwargs)


def output_directory_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an output directory path argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_output_directory
    Returns:
        Value validator function
    """
    return get_validator(validate_output_directory, **kwargs)


def output_file_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an output file path argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_output_file
    Returns:
        Value validator function
    """
    return get_validator(validate_output_file, **kwargs)


def str_arg(**kwargs: Any) -> Callable[[Any], str]:
    """Validate a string argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_str
    Returns:
        Value validator function
    """
    return get_validator(validate_str, **kwargs)
