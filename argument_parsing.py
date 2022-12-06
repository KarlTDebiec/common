#!/usr/bin/env python
#  Copyright 2017-2022 Karl T Debiec
#  All rights reserved. This software may be modified and distributed under
#  the terms of the BSD license. See the LICENSE file for details.
"""General-purpose functions related to argument parsing."""
from argparse import ArgumentParser, ArgumentTypeError, _ArgumentGroup
from pathlib import Path
from typing import Any, Callable

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
    return next(
        ag for ag in parser._action_groups if ag.title == "optional arguments"  # noqa
    )


def get_required_arguments_group(parser: ArgumentParser) -> _ArgumentGroup:
    """Get or create a 'required arguments' group from an argparser.

    Arguments:
        parser: Argparser to get group from
    Returns:
        Required arguments group
    """
    if any(
        (required := ag).title == "required arguments"
        for ag in parser._action_groups  # noqa
    ):
        return required  # noqa

    # Move "optional arguments" group below "required arguments" group
    optional = parser._action_groups.pop()  # noqa
    required = parser.add_argument_group("required arguments")
    parser._action_groups.append(optional)  # noqa

    return required


def get_validator(function: Callable, **kwargs: Any) -> Callable:
    """Get a function that can be called with the same signature as function.

    Arguments:
        function: Function to be wrapped
    Returns:
        Wrapped function
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
        **kwargs: Keyword arguments to pass to validate_float
    Returns:
        Value validator function
    """
    return get_validator(validate_float, **kwargs)


def input_directories_arg(**kwargs: Any) -> Callable[[Any], list[Path]]:
    """Validate an input directory paths argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_input_directory_paths
    Returns:
        Value validator function
    """
    return get_validator(validate_input_directories, **kwargs)


def input_directory_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an input directory path argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_input_directory_path
    Returns:
        Value validator function
    """
    return get_validator(validate_input_directory, **kwargs)


def input_file_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an input file path argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_input_file_path
    Returns:
        Value validator function
    """
    return get_validator(validate_input_file, **kwargs)


def input_files_arg(**kwargs: Any) -> Callable[[Any], list[Path]]:
    """Validate an input file paths argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_input_file_paths
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
        **kwargs: Keyword arguments to pass to validate_output_directory_path
    Returns:
        Value validator function
    """
    return get_validator(validate_output_directory, **kwargs)


def output_file_arg(**kwargs: Any) -> Callable[[Any], Path]:
    """Validate an output file path argument.

    Arguments:
        **kwargs: Keyword arguments to pass to validate_output_file_path
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
