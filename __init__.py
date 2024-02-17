#  Copyright 2017-2024 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""General-purpose code not tied to a particular project."""
from __future__ import annotations

from pathlib import Path

from .argument_parsing import (
    float_arg,
    get_arg_groups_by_name,
    get_optional_arguments_group,
    get_required_arguments_group,
    get_validator,
    input_directory_path_arg,
    input_directory_paths_arg,
    input_file_path_arg,
    input_file_paths_arg,
    int_arg,
    ints_arg,
    output_directory_path_arg,
    output_file_path_arg,
    str_arg,
)
from .cli import Cli
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
    rename_preexisting_output_path,
)
from .general import run_command, run_command_long
from .logging import set_logging_verbosity
from .testing import run_cli_with_args
from .typing import PathLike
from .validation import (
    validate_executable,
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
    validate_type,
)

package_root = Path(__file__).resolve().parent.parent
"""absolute path of package containing this common submodule (e.g. if this file is
'/path/to/package/common/__init__.py', value is '/path/to/package)"""

__all__ = [
    "ArgumentConflictError",
    "Cli",
    "DirectoryExistsError",
    "DirectoryNotFoundError",
    "ExecutableNotFoundError",
    "GetterError",
    "IsAFileError",
    "NotAFileError",
    "NotAFileOrDirectoryError",
    "PathLike",
    "UnsupportedPlatformError",
    "float_arg",
    "get_arg_groups_by_name",
    "get_optional_arguments_group",
    "get_required_arguments_group",
    "get_temp_directory_path",
    "get_temp_file_path",
    "get_validator",
    "input_directory_paths_arg",
    "input_directory_path_arg",
    "input_file_path_arg",
    "input_file_paths_arg",
    "int_arg",
    "ints_arg",
    "output_directory_path_arg",
    "output_file_path_arg",
    "package_root",
    "rename_preexisting_output_path",
    "run_cli_with_args",
    "run_command",
    "run_command_long",
    "set_logging_verbosity",
    "str_arg",
    "validate_executable",
    "validate_float",
    "validate_input_directory_path",
    "validate_input_directory_paths",
    "validate_input_file_path",
    "validate_input_file_paths",
    "validate_int",
    "validate_ints",
    "validate_output_directory_path",
    "validate_output_file_path",
    "validate_str",
    "validate_type",
]
