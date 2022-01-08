#!/usr/bin/env python
#   common/files.py
#
#   Copyright (C) 2017-2022 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""General-purpose functions for file interaction and manipulation not tied to
a particular project."""
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


def get_ext(filename: str) -> str:
    return splitext(basename(filename))[1].strip(".")


def get_name(filename: str) -> str:
    return splitext(basename(filename))[0]


def rename_preexisting_outfile(outfile: str) -> None:
    outfile = expandvars(outfile)
    if not isabs(outfile):
        outfile = join(getcwd(), outfile)
    outfile = normpath(outfile)
    directory = dirname(outfile)
    filename = get_name(outfile)
    extension = get_ext(outfile)
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
    try:
        f = NamedTemporaryFile(delete=False, suffix=suffix)
        f.close()
        remove(f.name)
        yield f.name
    finally:
        if isfile(f.name):
            remove(f.name)
