#!/usr/bin/env python
#   common/__init__.py
#
#   Copyright (C) 2017-2021 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""General-purpose code not tied to a particular project."""
####################################### MODULES ########################################
from pathlib import Path
from typing import List

from .cltool import CLTool
from .exceptions import (
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
from .files import get_ext, get_name, temporary_filename, rename_preexisting_outfile
from .misc import (
    embed_kw,
    get_shell_type,
    input_prefill,
)
from .validation import (
    validate_executable,
    validate_float,
    validate_input_path,
    validate_int,
    validate_output_path,
    validate_type,
)

###################################### VARIABLES #######################################
package_root: str = str(Path(__file__).parent.parent.absolute())
"""str: absolute path of package containing this common submodule (e.g. if this file is
'/path/to/test/common/__init__.py', value is '/path/to/test"""

######################################### ALL ##########################################
__all__: List[str] = [
    "ArgumentConflictError",
    "CLTool",
    "DirectoryExistsError",
    "DirectoryNotFoundError",
    "ExecutableNotFoundError",
    "GetterError",
    "IsAFileError",
    "NotAFileError",
    "NotAFileOrDirectoryError",
    "SetterError",
    "embed_kw",
    "get_ext",
    "get_name",
    "get_shell_type",
    "input_prefill",
    "package_root",
    "rename_preexisting_outfile",
    "temporary_filename",
    "validate_executable",
    "validate_float",
    "validate_input_path",
    "validate_int",
    "validate_output_path",
    "validate_type",
]
