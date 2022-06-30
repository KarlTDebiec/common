#!/usr/bin/env python
#  Copyright (C) 2017-2022. Karl T Debiec
#  All rights reserved. This software may be modified and distributed under
#  the terms of the BSD license. See the LICENSE file for details.
"""General-purpose validation functions not tied to a particular project."""
from enum import Enum
from logging import info
from os.path import defpath, expandvars
from pathlib import Path
from platform import system
from shutil import which
from typing import Any, Iterable, Optional, Type, Union

from .exception import (
    ArgumentConflictError,
    DirectoryNotFoundError,
    ExecutableNotFoundError,
    NotAFileError,
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
    value: Any, supported_platforms: Optional[set[str]] = None
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
                f"'{supported_platforms}' is of type '{type(value)}', not set[str]"
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


def validate_input_directory(path: Union[str, Path]) -> Path:
    """Validate input directory path and make it absolute.

    Arguments:
        path: Path to directory of input files
    Returns:
        Absolute path to input directory
    """
    path = Path(expandvars(str(path))).absolute()
    if not path.exists():
        raise DirectoryNotFoundError(f"Input directory {path} does not exist")
    if not path.is_dir():
        raise NotADirectoryError(f"Input directory {path} is not a directory")

    return path


def validate_input_directories(
    paths: Union[str, Path, Iterable[Union[str, Path]]]
) -> list[Path]:
    """Validate input directory paths and make them absolute.

    Arguments:
        paths: Path to directory or directories of input files
    Returns:
        List of absolute directory paths
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]
    validated_paths = []
    for path in paths:
        try:
            path = validate_input_directory(path)
        except (DirectoryNotFoundError, NotADirectoryError) as error:
            info(str(error))
            continue
        validated_paths.append(path)
    if len(validated_paths) == 0:
        raise DirectoryNotFoundError(f"No directories provided in {paths} exist")

    return validated_paths


def validate_input_file(path: Union[str, Path]) -> Path:
    """Validate input file path and make it absolute.

    Arguments:
        path: Path to input file
    Returns:
        Absolute path to input file
    """
    path = Path(expandvars(str(path))).absolute()
    if not path.exists():
        raise FileNotFoundError(f"Input file {path} does not exist")
    if not path.is_file():
        raise NotAFileError(f"Input file {path} is not a file")

    return path


def validate_input_files(
    paths: Union[str, Path, Iterable[Union[str, Path]]]
) -> list[Path]:
    """Validate input file paths and make them absolute.

    Arguments:
        paths: Paths to input file or files
    Returns:
        List of absolute file paths
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]
    validated_paths = []
    for path in paths:
        try:
            path = validate_input_file(path)
        except (FileNotFoundError, NotAFileError) as error:
            info(str(error))
            continue
        validated_paths.append(path)
    if len(validated_paths) == 0:
        raise FileNotFoundError(f"No files provided in {paths} exist")

    return validated_paths


def validate_int(
    value: Any,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    choices: Optional[tuple[int, ...]] = None,
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
    choices: Optional[tuple[int]] = None,
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


def validate_output_file(path: Union[str, Path], exists_ok=True) -> Path:
    """Validate output file path and make it absolute.

    Arguments:
        path: Output file path
        exists_ok: If True, do not raise an error if the file already exists
    Returns:
        Absolute path to output file
    """
    path = Path(expandvars(str(path))).absolute()
    if path.exists():
        if path.is_file():
            if not exists_ok:
                raise FileExistsError(f"{path} already exists")
            info(f"{path} already exists and may be overwritten")
            return path
        raise NotAFileError(f"{path} already exists and is not a file")
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
        info(f"Created directory {path.parent}")

    return path


def validate_output_directory(path: Union[str, Path]) -> Path:
    """Validate output directory path and make it absolute.

    Arguments:
        path: Output directory path
    Returns:
        Absolute to of output directory
    """
    path = Path(expandvars(str(path))).absolute()
    if path.exists():
        if not path.is_dir():
            raise NotADirectoryError(f"{path} already exists and is not a directory")
    else:
        path.mkdir(parents=True)
        info(f"Created directory {path}")

    return path


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
