#  Copyright 2017-2024 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""General-purpose validation functions not tied to a particular project."""
from __future__ import annotations

from logging import info
from os.path import defpath, expandvars
from pathlib import Path
from platform import system
from shutil import which
from typing import Any, Collection, Iterable

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


def validate_input_directory_path(path: PathLike, strict: bool = True) -> Path:
    """Resolve and validate input directory path.

    Arguments:
        path: path to directory of input files
        strict: raise error if directory does not exist
    Returns:
        resolved input directory path, with environment variables expanded
    Raises:
        DirectoryNotFoundError: input directory does not exist
        NotADirectoryError: input directory exists but is not a directory
    """
    path = Path(expandvars(str(path))).resolve()

    if path.exists():
        if not path.is_dir():
            raise NotADirectoryError(f"Input directory {path} is not a directory")
    elif strict:
        raise DirectoryNotFoundError(f"Input directory {path} does not exist")

    return path


def validate_input_directory_paths(
    paths: PathLike | Iterable[PathLike], strict: bool = True
) -> list[Path]:
    """Resolve and validate input directory paths.

    Arguments:
        paths: path to directory or directories of input files
        strict: raise error if any directory does not exist
    Returns:
        resolved input directory paths, with environment variables expanded
    Raises:
        DirectoryNotFoundError: an input directory does not exist
        NotADirectoryError: an input directory exists but is not a directory
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]

    validated_paths = [
        validate_input_directory_path(path, strict=strict) for path in paths
    ]

    return validated_paths


def validate_input_file_path(path: PathLike, strict: bool = True) -> Path:
    """Resolve and validate input file path.

    Arguments:
        path: path to input file
        strict: raise error if file does not exist
    Returns:
        resolved input file path, with environment variables expanded
    Raises:
        FileNotFoundError: input file does not exist
        NotAFileError: input file exists but is not a file
    """
    path = Path(expandvars(str(path))).resolve()

    if path.exists():
        if not path.is_file():
            raise NotAFileError(f"Input file {path} is not a file")
    elif strict:
        raise FileNotFoundError(f"Input file {path} does not exist")

    return path


def validate_input_file_paths(
    paths: PathLike | Iterable[PathLike], strict: bool = True
) -> list[Path]:
    """Resolve and validate input file paths.

    Arguments:
        paths: paths to input file or files
        strict: raise error if any file does not exist
    Returns:
        resolved input file paths, with environment variables expanded
    Raises:
        FileNotFoundError: an input file does not exist
        NotAFileError: an input file exists but is not a file
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]

    validated_paths = [validate_input_file_path(path, strict=strict) for path in paths]

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

    validated_values = []
    for value in values:
        validated_values.append(validate_int(value, min_value, max_value, options))

    if length and len(validated_values) != length:
        raise ValueError(
            f"'{validated_values}' is of length {len(validated_values)}, not "
            f"'{min_value}'"
        )

    return validated_values


def validate_output_file_path(
    path: PathLike, strict: bool = True, parents: bool = True
) -> Path:
    """Validate output file path and make it absolute.

    Arguments:
        path: output file path
        strict: raise error if file already exists
        parents: create parent directories if they do not exist
    Returns:
        resolved path to output file, with environment variables expanded
    Raises:
        DirectoryNotFoundError: parent directory does not exist
        FileExistsError: output file already exists
        NotAFileError: output file already exists but is not a file
    """
    path = Path(expandvars(str(path))).resolve()

    if path.exists():
        if strict:
            raise FileExistsError(f"Output file {path} already exists")
        if not path.is_file():
            raise NotAFileError(f"Output file {path} already exists but is not a file")
    if not path.parent.exists():
        if not parents:
            raise DirectoryNotFoundError(
                f"Output file {path} parent {path.parent} does not exist"
            )
        path.parent.mkdir(parents=True)
        info(f"Created directory {path.parent}")

    return path


def validate_output_directory_path(
    path: PathLike,
) -> Path:
    """Validate output directory path and make it absolute.

    Arguments:
        path: output directory path
    Returns:
        Absolute path to output directory, with environment variables expanded
    Raises:
        NotADirectoryError: output directory already exists but is not a directory
    """
    path = Path(expandvars(str(path))).resolve()
    if path.exists():
        if not path.is_dir():
            raise NotADirectoryError(
                f"Output directory {path} already exists but is not a directory"
            )
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
