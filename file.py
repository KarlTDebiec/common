#!/usr/bin/env python
#  Copyright 2017-2023 Karl T Debiec
#  All rights reserved. This software may be modified and distributed under
#  the terms of the BSD license. See the LICENSE file for details.
"""General-purpose functions for file interaction and manipulation."""
from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from logging import debug, info
from os import remove
from pathlib import Path
from shutil import move, rmtree
from tempfile import NamedTemporaryFile, mkdtemp
from typing import Optional


def rename_preexisting_output_file_path(output_path: Path) -> None:
    """Check if a proposed outfile exists, and if so rename the existing file.

    Arguments:
        output_path: Path to proposed output file
    """
    output_path = output_path.resolve()
    if output_path.exists():
        backup_i = 0
        while True:
            backup_path = output_path.with_stem(f"{output_path.stem}_{backup_i:03d}")
            if not backup_path.exists():
                info(f"Moving pre-existing file {output_path} to {backup_path}")
                move(output_path, backup_path)
                break
            backup_i += 1


@contextmanager
def get_temp_directory_path() -> Generator[Path, None, None]:
    """Provide path to a temporary directory and remove it once no longer needed."""
    temp_directory_path = None
    try:
        temp_directory_path = mkdtemp()
        yield Path(temp_directory_path).resolve()
    finally:
        if temp_directory_path is not None:
            rmtree(temp_directory_path)


@contextmanager
def get_temp_file_path(suffix: Optional[str] = None) -> Generator[Path, None, None]:
    """Provide path to a temporary file and remove it once no longer needed.

    Arguments:
        suffix: Suffix of named temporary file
    """
    temp_file_path = None
    try:
        temp_file = NamedTemporaryFile(delete=False, suffix=suffix)
        temp_file.close()
        temp_file_path = Path(temp_file.name)
        remove(temp_file_path)
        yield temp_file_path
    finally:
        if temp_file_path is not None and temp_file_path.exists():
            try:
                remove(temp_file_path)
            except PermissionError as error:
                debug(
                    f"temp_file_path encountered PermissionException '{error}'; "
                    f"temporary file {temp_file_path}, will not be removed."
                )
