#  Copyright 2017-2025 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""General-purpose validation functions not tied to a particular project."""

from __future__ import annotations

from collections.abc import Collection, Iterable
from logging import info
from os.path import defpath, expanduser, expandvars
from pathlib import Path
from platform import system
from shutil import which
from typing import Any

from .exception import (
    ArgumentConflictError,
    DirectoryNotFoundError,
    ExecutableNotFoundError,
    NotAFileError,
    UnsupportedPlatformError,
)
from .typing import PathLike


def validate_executable(
    name: str, supported_platforms: Collection[str] | None = None
) -> Path:
    """Validates that executable name and returns its absolute path.

    Arguments:
        name: executable name
        supported_platforms: Platforms that support executable;
          default: "Darwin", "Linux", "Windows"
    Returns:
        Absolute path of executable
    Raises:
        ExecutableNotFoundError: if executable is not found in path
        UnsupportedPlatformError: if executable is not supported on current platform
    """
    if supported_platforms is None:
        supported_platforms = {"Darwin", "Linux", "Windows"}

    if system() not in supported_platforms:
        raise UnsupportedPlatformError(
            f"Executable '{name}' is not supported on {system()}"
        )

    which_executable = which(name)
    if not which_executable:
        raise ExecutableNotFoundError(f"Executable '{name}' not found in '{defpath}'")
    executable_path = Path(which_executable).resolve()

    return executable_path


def validate_float(
    value: Any, min_value: float | None = None, max_value: float | None = None
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
        ValueError: If value is less than min_value or greater than max_value
    """
    if min_value and max_value and (min_value >= max_value):
        raise ArgumentConflictError("min_value must be greater than max_value")

    try:
        return_value = float(value)
    except ValueError as error:
        raise TypeError(
            f"{value} is of type {type(value)}, cannot be cast to int"
        ) from error

    if min_value and return_value < min_value:
        raise ValueError(f"{return_value} is less than minimum value of {min_value}")
    if max_value and return_value > max_value:
        raise ValueError(f"{return_value} is greater than maximum value of {max_value}")

    return return_value


def validate_input_directory(path: PathLike) -> Path:
    """Validate input directory path, expand '~' and env vars, and make it absolute.

    Arguments:
        path: Path to directory of input files
    Returns:
        Absolute path to input directory
    """
    path = Path(expandvars(expanduser(str(path)))).absolute().resolve()
    if not path.exists():
        raise DirectoryNotFoundError(f"Input directory {path} does not exist")
    if not path.is_dir():
        raise NotADirectoryError(f"Input directory {path} is not a directory")

    return path


def validate_input_directories(paths: PathLike | Iterable[PathLike]) -> list[Path]:
    """Validate input directory paths and make them absolute.

    Arguments:
        paths: Path to directory or directories of input files
    Returns:
        List of absolute directory paths
    """
    if isinstance(paths, (str | Path)):
        paths = [paths]
    validated_paths = []
    for path in paths:
        try:
            validated_path = validate_input_directory(path)
        except (DirectoryNotFoundError, NotADirectoryError) as error:
            info(str(error))
            continue
        validated_paths.append(validated_path)
    if len(validated_paths) == 0:
        raise DirectoryNotFoundError(f"No directories provided in {paths} exist")

    return validated_paths


def validate_input_file(path: PathLike, must_exist: bool = True) -> Path:
    """Validate input file path, expand '~' and env vars, and make it absolute.

    Arguments:
        path: Path to input file
        must_exist: If True, do not raise an error if the file does not exist
    Returns:
        Absolute path to input file
    """
    path = Path(expandvars(expanduser(str(path)))).absolute().resolve()
    if path.exists():
        if not path.is_file():
            raise NotAFileError(f"Input file {path} is not a file")
    elif must_exist:
        raise FileNotFoundError(f"Input file {path} does not exist")

    return path


def validate_input_files(paths: PathLike | Iterable[PathLike]) -> list[Path]:
    """Validate input file paths and make them absolute.

    Arguments:
        paths: Paths to input file or files
    Returns:
        List of absolute file paths
    """
    if isinstance(paths, (str | Path)):
        paths = [paths]
    validated_paths = []
    for path in paths:
        try:
            validated_path = validate_input_file(path)
        except (FileNotFoundError, NotAFileError) as error:
            info(str(error))
            continue
        validated_paths.append(validated_path)
    if len(validated_paths) == 0:
        raise FileNotFoundError(f"No files provided in {paths} exist")

    return validated_paths


def validate_int(
    value: Any,
    min_value: int | None = None,
    max_value: int | None = None,
    options: Collection[int] | None = None,
) -> int:
    """Validate an int.

    Arguments:
        value: Input value to validate
        min_value: Minimum value of int, if applicable
        max_value: Maximum value of int, if applicable
        options: Acceptable int values, if applicable
    Returns:
        value as an int
    Raises:
        ArgumentConflictError: If min_value is greater than max_value
        TypeError: If value may not be cast to an int
        ValueError: If value is less than min_value or greater than max_value, or is not
          one of the provided options
    """
    if min_value and max_value and (min_value >= max_value):
        raise ArgumentConflictError("min_value must be greater than max_value")

    try:
        return_value = int(value)
    except ValueError as error:
        raise TypeError(
            f"{value} is of type {type(value)}, cannot be cast to float"
        ) from error

    if min_value and return_value < min_value:
        raise ValueError(f"{return_value} is less than minimum value of {min_value}")
    if max_value and return_value > max_value:
        raise ValueError(f"{return_value} is greater than maximum value of {max_value}")
    if options and return_value not in options:
        raise ValueError(f"{return_value} is not one of {options}")

    return return_value


def validate_ints(
    values: Any,
    length: int | None = None,
    min_value: int | None = None,
    max_value: int | None = None,
    options: Collection[int] | None = None,
):
    """Validate a collection of int.

    Arguments:
        values: Input values to validate
        length:  Number of values expected, if applicable
        min_value: Minimum value of int, if applicable
        max_value: Maximum value of int, if applicable
        options: Acceptable int values, if applicable
    Returns:
        values as a list of ints
    Raises:
        ArgumentConflictError: If min_value is greater than max_value
        ValueError: If value is less than min_value or greater than max_value
    """
    if min_value and max_value and (min_value >= max_value):
        raise ArgumentConflictError("min_value must be greater than max_value")

    try:
        len(values)
    except TypeError:
        values = [values]

    validated_values = [
        validate_int(value, min_value, max_value, options) for value in values
    ]

    if length and len(validated_values) != length:
        raise ValueError(
            f"'{validated_values}' is of length {len(validated_values)}, not "
            f"'{min_value}'"
        )

    return validated_values


def validate_output_file(path: PathLike, may_exist: bool = True) -> Path:
    """Validate output file path, expand '~' and env vars, and make it absolute.

    Arguments:
        path: Output file path
        may_exist: If True, do not raise an error if the file already exists
    Returns:
        Absolute path to output file
    """
    path = Path(expandvars(expanduser(str(path)))).absolute().resolve()
    if path.exists():
        if path.is_file():
            if not may_exist:
                raise FileExistsError(f"{path} already exists")
            info(f"{path} already exists and may be overwritten")
            return path
        raise NotAFileError(f"{path} already exists and is not a file")
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
        info(f"Created directory {path.parent}")

    return path


def validate_output_directory(path: PathLike) -> Path:
    """Validate output directory path, expand '~' and env vars, and make it absolute.

    Arguments:
        path: Output directory path
    Returns:
        Absolute path to output directory
    """
    path = Path(expandvars(expanduser(str(path)))).absolute().resolve()
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
            validated_option = str(option)
        except ValueError:
            raise ArgumentConflictError(
                f"Option '{option}' is of type '{type(option)}', not str"
            ) from None
        case_insensitive_options[validated_option.lower()] = validated_option

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


__all__ = [
    "validate_executable",
    "validate_float",
    "validate_input_directories",
    "validate_input_directory",
    "validate_input_file",
    "validate_input_files",
    "validate_int",
    "validate_ints",
    "validate_output_directory",
    "validate_output_file",
    "validate_str",
    "validate_type",
]
