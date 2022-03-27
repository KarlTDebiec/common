#!/usr/bin/env python
#   Copyright (C) 2017-2022 Karl T Debiec
#   All rights reserved. This software may be modified and distributed under
#   the terms of the BSD license. See the LICENSE file for details.
"""General-purpose validation functions not tied to a particular project."""
from enum import Enum
from functools import partial
from os import R_OK, W_OK, access, getcwd, makedirs
from os.path import (
    defpath,
    dirname,
    exists,
    expandvars,
    isabs,
    isdir,
    isfile,
    join,
    normpath,
)
from platform import system
from shutil import which
from typing import Any, Iterable, Optional, Set, Tuple, Type

from .exception import (
    ArgumentConflictError,
    DirectoryNotFoundError,
    ExecutableNotFoundError,
    NotAFileError,
    NotAFileOrDirectoryError,
    UnsupportedPlatformError,
)


def validate_enum(value: Any, enum: Type[Enum]) -> Enum:
    """Validate an enum member, if necessary converted from a string.

    Arguments:
        value: Member name
        enum: Enum
    Returns:
        validated enum member
    Raises:
        TypeError: If enum is not an Enum, or value is not a member of enum
    """
    if not isinstance(enum, type(Enum)):
        raise TypeError(f"'{enum}' is of type '{type(enum)}', not Enum")
    if isinstance(value, enum):
        return value
    value = str(value)
    if value.startswith(Enum.__name__):
        value = value[len(Enum.__name__) :].lstrip(".")
    if hasattr(enum, value):
        return enum[value]

    raise TypeError(
        f"{value} is not a member of {enum.__name__}, must be one of "
        f"{list(enum.__members__.keys())}"
    )


def validate_executable(
    value: Any, supported_platforms: Optional[Set[str]] = None
) -> str:
    """Validates that executable name and returns its absolute path.

    Arguments:
        value: executable name
        supported_platforms: Platforms that support executable;
          default: "Darwin", "Linux", "Windows"
    Returns:
        Absolute path of executable
    Raises:
        ExecutableNotFoundError: if executable is not found in path
        TypeError: if value or supported platform are not of the expected types
        UnsupportedPlatformError: if executable is not supported on current platform
    """
    try:
        value = str(value)
    except ValueError:
        raise TypeError(f"'{value}' is of type '{type(value)}', not str") from None
    if supported_platforms is None:
        supported_platforms = {"Darwin", "Linux", "Windows"}
    else:
        try:
            supported_platforms = set(supported_platforms)
        except ValueError:
            raise TypeError(
                f"'{supported_platforms}' is of type '{type(value)}', not Set[str]"
            ) from None

    if system() not in supported_platforms:
        raise UnsupportedPlatformError(
            f"Executable '{value}' is not supported on {system()}"
        )

    which_value = which(value)
    if which_value is None:
        raise ExecutableNotFoundError(f"Executable '{value}' not found in '{defpath}'")

    return which_value


def validate_float(
    value: Any, min_value: Optional[float] = None, max_value: Optional[float] = None
) -> float:
    """Validate a float.

    Arguments:
        value: Input value to validate
        min_value: Minimum value of float, if applicable
        max_value: Maximum value of float, if applicable
    Returns:
        value as a float
    Raises:
        ArgumentConflictError: If min_value is greater than max_value
        TypeError: If value may not be cast to a float
        ValueError: If value is less than min_value or greater than max_value
    """
    if min_value is not None and max_value is not None and (min_value >= max_value):
        raise ArgumentConflictError("min_value must be greater than max_value")

    try:
        value = float(value)
    except ValueError:
        raise TypeError(f"'{value}' is of type '{type(value)}', not float") from None

    if min_value is not None and value < min_value:
        raise ValueError(f"{value} is less than minimum value of {min_value}")
    if max_value is not None and value > max_value:
        raise ValueError(f"{value} is greater than maximum value of {max_value}")

    return value


def validate_input_path(
    value: Any,
    file_ok: bool = True,
    directory_ok: bool = False,
    default_directory: Optional[str] = None,
    create_directory: bool = False,
) -> str:
    """Validate an input path and make it absolute.

    Arguments:
        value: Input value to validate
        file_ok: Whether file paths are permissible
        directory_ok: Whether directory paths are permissible
        default_directory: Default directory to prepend to *value* if not absolute;
          default: current working directory
        create_directory: Whether to create directory if it does not already exist
    Returns:
        Absolute path to input file or directory
    Raises:
        ArgumentConflictError: If neither *file_ok* nor *directory_ok*
        FileNotFoundError: If *value* does not exist
        NotADirectoryError: If *directory_ok* and not *file_ok* and *value* exists but
          is not a directory
        NotAFileError: If *file_ok* and not *directory_ok* and *value* exists but is
          not a file
        NotAFileOrDirectoryError: If *file_ok* and _directory_ok* and *value* exists but
          is not a file or directory
        PermissionError: If *value* cannot be read
        TypeError: If *value* cannot be cast to a string
    """
    if not file_ok and not directory_ok:
        raise ArgumentConflictError(
            "both file and directory paths may not be prohibited"
        )
    if default_directory is None:
        default_directory = getcwd()

    try:
        value = str(value)
    except ValueError:
        raise TypeError(f"'{value}' is of type '{type(value)}', not str") from None

    value = expandvars(value)
    if not isabs(value):
        value = join(default_directory, value)
    value = normpath(value)

    if not exists(value):
        if directory_ok and create_directory:
            makedirs(value)
        else:
            if not file_ok and directory_ok:
                raise DirectoryNotFoundError(f"'{value}' does not exist")
            raise FileNotFoundError(f"'{value}' does not exist")
    if file_ok and not directory_ok and not isfile(value):
        raise NotAFileError(f"'{value}' is not a file")
    if not file_ok and directory_ok and not isdir(value):
        raise NotADirectoryError(f"'{value}' is not a directory")
    if not isfile(value) and not isdir(value):
        raise NotAFileOrDirectoryError(f"'{value}' is not a file or directory")
    if not access(value, R_OK):
        raise PermissionError(f"'{value}' cannot be read")

    return value


def validate_int(
    value: Any,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    choices: Optional[Tuple[int, ...]] = None,
) -> int:
    """Validate an int.

    Arguments:
        value: Input value to validate
        min_value: Minimum value of int, if applicable
        max_value: Maximum value of int, if applicable
        choices: Acceptable int values, if applicable
    Returns:
        value as an int
    Raises:
        ArgumentConflictError: If min_value is greater than max_value
        TypeError: If value may not be cast to an int
        ValueError: If value is less than min_value or greater than max_value, or is not
          one of the provided options
    """
    if min_value is not None and max_value is not None and (min_value >= max_value):
        raise ArgumentConflictError("min_value must be greater than max_value")

    try:
        value = int(value)
    except ValueError:
        raise TypeError(f"'{value}' is of type '{type(value)}', not int") from None

    if min_value is not None and value < min_value:
        raise ValueError(f"{value} is less than minimum value of {min_value}")
    if max_value is not None and value > max_value:
        raise ValueError(f"{value} is greater than maximum value of {max_value}")
    if choices is not None and value not in choices:
        raise ValueError(f"{value} is not one of {choices}")

    return value


def validate_ints(
    values: Any,
    length: Optional[int] = None,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    choices: Optional[Tuple[int]] = None,
):
    """Validate a collection of int.

    Arguments:
        values: Input values to validate
        length:  Number of values expected, if applicable
        min_value: Minimum value of int, if applicable
        max_value: Maximum value of int, if applicable
        choices: Acceptable int values, if applicable
    Returns:
        values as a list of ints
    Raises:
        ArgumentConflictError: If min_value is greater than max_value
        ValueError: If value is less than min_value or greater than max_value
    """
    if min_value is not None and max_value is not None and (min_value >= max_value):
        raise ArgumentConflictError("min_value must be greater than max_value")

    try:
        len(values)
    except TypeError:
        values = [values]

    validated_values = []
    for value in values:
        validated_values.append(validate_int(value, min_value, max_value, choices))

    if length is not None and len(validated_values) != length:
        raise ValueError(
            f"'{validated_values}' is of length {len(validated_values)}, not "
            f"'{min_value}'"
        )

    return validated_values


def validate_output_path(
    value: Any,
    file_ok: bool = True,
    directory_ok: bool = False,
    default_directory: Optional[str] = None,
    create_directory: bool = False,
) -> str:
    """Validate an output path and makes it absolute.

    Arguments:
        value: Provided output path
        file_ok: Whether file paths are permissible
        directory_ok: Whether directory paths are permissible
        default_directory: Default directory to prepend to *value* if not absolute;
          default: current working directory
        create_directory: Create output directory if it does not already exist
    Returns:
        str: Absolute path to output file or directory
    Raises:
        ArgumentConflictError: If neither *file_ok* nor *directory_ok*
        DirectoryNotFoundError: If *value*'s containing directory does not exist
        NotADirectoryError: If *directory_ok* and not *file_ok* and *value* exists but
          is not a directory, or if *value's* containing directory is not a directory
        NotAFileError: If *file_ok* and not *directory_ok* and *value* exists but is
          not a file
        NotAFileOrDirectoryError: If *file_ok* and _directory_ok* and *value* exists but
          is not a file or directory
        PermissionError: If *value* exists and cannot be written, or if *value*'s
          containing directory exists but is not a directory
        TypeError: If *value* cannot be cast to a string
    """
    if not file_ok and not directory_ok:
        raise ArgumentConflictError(
            "Arguments 'file_ok' and 'directory_ok' are in conflict; both file and "
            "directory paths may not be prohibited"
        )
    if not directory_ok and create_directory:
        raise ArgumentConflictError(
            "Arguments 'directory_ok' and 'create_directory' "
            "are in conflict; may not prohibit directory paths and enable directory "
            "creation"
        )
    if default_directory is None:
        default_directory = getcwd()

    try:
        value = str(value)
    except ValueError:
        raise TypeError(f"'{value}' is of type '{type(value)}', not str") from None

    value = expandvars(value)
    if not isabs(value):
        value = join(default_directory, value)
    value = normpath(value)

    if exists(value):
        if file_ok and not directory_ok and not isfile(value):
            raise NotAFileError(f"'{value}' is not a file")
        if not file_ok and directory_ok and not isdir(value):
            raise NotADirectoryError(f"'{value}' is not a directory")
        if not isfile(value) and not isdir(value):
            raise NotAFileOrDirectoryError(f"'{value}' is not a file or directory")
        if not access(value, W_OK):
            raise PermissionError(f"'{value}' cannot be written")
    else:
        if create_directory:
            makedirs(value)
        else:
            directory = dirname(value)
            if not exists(directory):
                raise DirectoryNotFoundError(f"'{directory}' does not exist")
            if not isdir(directory):
                raise NotADirectoryError(f"'{directory}' is not a directory")
            if not access(directory, W_OK):
                raise PermissionError(f"'{directory}' cannot be written")

    return value


def validate_str(value: Any, options: Iterable[str]) -> str:
    """Validate a str.

    Arguments:
        value: Input value to validate
        options: Acceptable string values, if applicable
    Returns:
        Value as a str
    Raises:
        ArgumentConflictError: If an option cannot be cast to a string
        TypeError: If value may not be cast to a str
        ValueError: If value is not one of the provided options
    """
    case_insensitive_options = {}
    for option in options:
        try:
            option = str(option)
        except ValueError:
            raise ArgumentConflictError(
                f"Option '{option}' is of type '{type(option)}', not str"
            ) from None
        case_insensitive_options[option.lower()] = option

    try:
        value = str(value)
    except ValueError:
        raise TypeError(f"'{value}' is of type '{type(value)}', not str") from None
    value = value.lower()

    if value not in case_insensitive_options:
        raise ValueError(
            f"'{value}' is not one of options '{case_insensitive_options.keys()}'"
        ) from None

    return case_insensitive_options[value]


def validate_type(value: Any, cls: Any) -> Any:
    """Validate that value is of type cls.

    Arguments:
        value: Input object to validate
        cls: Required type of object
    Returns:
        value
    Raises:
        TypeError: If value is not of type cls
    """
    if not isinstance(value, cls):
        raise TypeError(f"'{value}' is of type '{type(value)}', not {cls.__name__}")
    return value


validate_input_directory = partial(
    validate_input_path, file_ok=False, directory_ok=True
)
"""Validate an input directory path and make it absolute"""

validate_input_file = partial(validate_input_path, file_ok=True, directory_ok=False)
"""Validate an input file path and make it absolute"""

validate_output_directory = partial(
    validate_output_path,
    file_ok=False,
    directory_ok=True,
)
"""Validate an output directory path and make it absolute"""

validate_output_file = partial(validate_output_path, file_ok=True, directory_ok=False)
"""Validate an output file path and make it absolute"""
