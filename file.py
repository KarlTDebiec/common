#!/usr/bin/env python
#  Copyright (C) 2020-2022. Karl T Debiec
#  All rights reserved. This software may be modified and distributed under
#  the terms of the BSD license. See the LICENSE file for details.
"""General-purpose functions for file interaction and manipulation."""
from contextlib import contextmanager
from logging import debug, info
from os import getcwd, remove, rename
from os.path import (
    basename,
    dirname,
    exists,
    expandvars,
    isabs,
    isfile,
    join,
    normpath,
    splitext,
)
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Optional


def rename_preexisting_outfile(outfile: str) -> None:
    """Check if a proposed outfile exists, and if so rename the existing file.

    Arguments:
        outfile: Proposed outfile
    """
    outfile = expandvars(outfile)
    if not isabs(outfile):
        outfile = join(getcwd(), outfile)
    outfile = normpath(outfile)
    directory = dirname(outfile)
    filename = splitext(basename(outfile))[0]
    extension = splitext(basename(outfile))[1].strip(".")
    if exists(outfile):
        backup_i = 0
        while True:
            backup_outfile = join(directory, f"{filename}_{backup_i:03d}.{extension}")
            if not exists(backup_outfile):
                info(f"Moving up '{outfile}' to '{backup_outfile}'")
                debug(f"Moving up '{outfile}' to '{backup_outfile}'")
                rename(outfile, backup_outfile)
                break
            backup_i += 1


@contextmanager
def temporary_filename(suffix: Optional[str] = None) -> None:
    """Provide a named temporary file and remove it once no longer needed.

    Arguments:
        suffix: Suffix of named temporary file
    """
    named_temporary_file = None
    try:
        named_temporary_file = NamedTemporaryFile(delete=False, suffix=suffix)
        named_temporary_file.close()
        remove(named_temporary_file.name)
        yield named_temporary_file.name
    finally:
        if named_temporary_file is not None:
            if isfile(named_temporary_file.name):
                try:
                    remove(named_temporary_file.name)
                except PermissionError as error:
                    debug(
                        f"temporary_filename encountered PermissionException "
                        f"'{error}'; temporary file '{named_temporary_file.name}', "
                        f"will not be removed."
                    )


@contextmanager
def temp_file(suffix: Optional[str] = None) -> None:
    """Provide path to a temporary file and remove it once no longer needed.

    Arguments:
        suffix: Suffix of named temporary file
    """
    temp_file = None
    try:
        temp_file = NamedTemporaryFile(delete=False, suffix=suffix)
        temp_file.close()
        remove(temp_file)
        yield Path(temp_file)
    finally:
        if temp_file is not None and temp_file.exists():
            try:
                remove(temp_file)
            except PermissionError as error:
                debug(
                    f"temp_file_path encountered PermissionException '{error}'; "
                    f"temporary file '{temp_file}', will not be removed."
                )


@contextmanager
def temp_directory() -> None:
    """Provide path to a temporary directory and remove it once no longer needed."""
    temp_directory = None
    try:
        temp_directory = TemporaryDirectory()
        yield Path(temp_directory.name)
    finally:
        if temp_directory is not None:
            temp_directory.cleanup()
