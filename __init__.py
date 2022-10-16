#!/usr/bin/env python
#  Copyright 2017-2022 Karl T Debiec
#  All rights reserved. This software may be modified and distributed under
#  the terms of the BSD license. See the LICENSE file for details.
"""General-purpose code not tied to a particular project."""
from pathlib import Path

from .command_line_interface import CommandLineInterface
from .exception import (
    ArgumentConflictError,
    DirectoryExistsError,
    DirectoryNotFoundError,
    ExecutableNotFoundError,
    GetterError,
    IsAFileError,
    NotAFileError,
    NotAFileOrDirectoryError,
    UnsupportedPlatformError,
)
from .file import (
    get_temp_directory_path,
    get_temp_file_path,
    rename_preexisting_output_file_path,
)
from .general import run_command, set_logging_verbosity
from .validation import (
    validate_enum,
    validate_executable,
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
    validate_type,
)

package_root = Path(__file__).resolve().parent.parent
"""absolute path of package containing this common submodule (e.g. if this file is
'/path/to/package/common/__init__.py', value is '/path/to/package"""

__all__: list[str] = [
    "ArgumentConflictError",
    "CommandLineInterface",
    "DirectoryExistsError",
    "DirectoryNotFoundError",
    "ExecutableNotFoundError",
    "GetterError",
    "IsAFileError",
    "NotAFileError",
    "NotAFileOrDirectoryError",
    "UnsupportedPlatformError",
    "package_root",
    "rename_preexisting_output_file_path",
    "run_command",
    "set_logging_verbosity",
    "get_temp_directory_path",
    "get_temp_file_path",
    "validate_enum",
    "validate_executable",
    "validate_float",
    "validate_input_directory",
    "validate_input_directories",
    "validate_input_file",
    "validate_input_files",
    "validate_int",
    "validate_ints",
    "validate_output_directory",
    "validate_output_file",
    "validate_str",
    "validate_type",
]
