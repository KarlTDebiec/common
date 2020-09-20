#!/usr/bin/env python
#   common/__init__.py
#
#   Copyright (C) 2017-2020 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
General-purpose code not tied to a particular project.

Last updated 2020-09-16.
"""
####################################### MODULES ########################################
from pathlib import Path

###################################### VARIABLES #######################################
package_root: str = str(Path(__file__).parent.parent.absolute())
"""str: absolute path of package containing this common submodule (e.g. if common is a
submodule of the 'test' package, value is '/path/to/test"""

####################################### MODULES ########################################
from typing import List

from .cltool import CLTool
from .general import (
    embed_kw,
    get_ext,
    get_name,
    get_shell_type,
    input_prefill,
    temporary_filename,
    validate_executable,
    validate_float,
    validate_input_path,
    validate_int,
    validate_output_path,
    validate_type,
    ArgumentConflictError,
    DirectoryExistsError,
    DirectoryNotFoundError,
    ExecutableNotFoundError,
    GetterError,
    IsAFileError,
    NotAFileError,
    NotAFileOrDirectoryError,
    SetterError,
)

######################################### ALL ##########################################
__all__: List[str] = [
    "CLTool",
    "embed_kw",
    "get_ext",
    "get_name",
    "get_shell_type",
    "input_prefill",
    "package_root",
    "temporary_filename",
    "validate_executable",
    "validate_float",
    "validate_input_path",
    "validate_int",
    "validate_output_path",
    "validate_type",
    "ArgumentConflictError",
    "DirectoryExistsError",
    "DirectoryNotFoundError",
    "ExecutableNotFoundError",
    "GetterError",
    "IsAFileError",
    "NotAFileError",
    "NotAFileOrDirectoryError",
    "SetterError",
]
