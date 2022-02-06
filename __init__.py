#!/usr/bin/env python
#   common/__init__.py
#
#   Copyright (C) 2017-2022 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""General-purpose code not tied to a particular project."""
from pathlib import Path
from typing import List

from .command_line_tool import CommandLineTool
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
from .general import get_shell_type, input_prefill, run_command
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

package_root: str = str(Path(__file__).parent.parent.absolute())
"""str: absolute path of package containing this common submodule (e.g. if this file is
'/path/to/test/common/__init__.py', value is '/path/to/test"""

__all__: List[str] = [
    "ArgumentConflictError",
    "CommandLineTool",
    "DirectoryExistsError",
    "DirectoryNotFoundError",
    "ExecutableNotFoundError",
    "GetterError",
    "IsAFileError",
    "NotAFileError",
    "NotAFileOrDirectoryError",
    "SetterError",
    "UnsupportedPlatformError",
    "get_shell_type",
    "input_prefill",
    "package_root",
    "rename_preexisting_outfile",
    "run_command",
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
