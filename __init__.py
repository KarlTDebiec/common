#!/usr/bin/env python
#   Copyright (C) 2017-2022 Karl T Debiec
#   All rights reserved. This software may be modified and distributed under
#   the terms of the BSD license. See the LICENSE file for details.
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
    SetterError,
    UnsupportedPlatformError,
)
from .file import rename_preexisting_outfile, temporary_filename
from .general import run_command, set_logging_verbosity
from .validation import (
    validate_enum,
    validate_executable,
    validate_float,
    validate_input_directory,
    validate_input_file,
    validate_input_path,
    validate_int,
    validate_ints,
    validate_output_directory,
    validate_output_file,
    validate_output_path,
    validate_str,
    validate_type,
)

package_root = Path(__file__).parent.parent.absolute()
"""absolute path of package containing this common submodule (e.g. if this file is
'/path/to/test/common/__init__.py', value is '/path/to/test"""

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
    "SetterError",
    "UnsupportedPlatformError",
    "package_root",
    "rename_preexisting_outfile",
    "run_command",
    "set_logging_verbosity",
    "temporary_filename",
    "validate_enum",
    "validate_executable",
    "validate_float",
    "validate_input_directory",
    "validate_input_file",
    "validate_input_path",
    "validate_int",
    "validate_ints",
    "validate_output_directory",
    "validate_output_file",
    "validate_output_path",
    "validate_str",
    "validate_type",
]
