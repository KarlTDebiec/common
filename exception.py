#!/usr/bin/env python
#   common/exception.py
#
#   Copyright (C) 2017-2022 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""General-purpose exceptions."""
from inspect import currentframe, getframeinfo


class ArgumentConflictError(Exception):
    """Two or more arguments are in conflict with one another."""


class DirectoryExistsError(OSError):
    """Directory already exists."""


class DirectoryNotFoundError(OSError):
    """Directory not found."""


class ExecutableNotFoundError(OSError):
    """Executable not found."""


class GetterError(TypeError):
    """Error encountered in getter method."""


class IsAFileError(OSError):
    """Is a file."""


class NotAFileError(OSError):
    """Is not a file."""


class NotAFileOrDirectoryError(OSError):
    """Is not a file or directory."""


class SetterError(TypeError):
    """Error encountered in setter method."""

    def __init__(self, cls: object, value: object):
        """Initialize.

        Arguments:
            cls: Class to which setter belongs
            value: Value passed to setter
        """
        super().__init__()

        cls_type_name = type(cls).__name__
        prop_name = getframeinfo(currentframe().f_back).function
        value_type_name = type(value).__name__
        prop_docstring = getattr(type(cls), prop_name).__doc__
        prop_docstring = prop_docstring.split(":")[0]

        self.message = (
            f"Property '{cls_type_name}.{prop_name}' was passed invalid value "
            f"'{value}' of type '{value_type_name}'. Expects '{prop_docstring}'."
        )

    def __str__(self) -> str:
        """String representation."""
        return self.message


class UnsupportedPlatformError(OSError):
    """Platform is unsupported."""
