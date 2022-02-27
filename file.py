#!/usr/bin/env python
#   common/file.py
#
#   Copyright (C) 2017-2022 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
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
from tempfile import NamedTemporaryFile
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
                remove(named_temporary_file.name)
