#!/usr/bin/env python
#   Copyright (C) 2017-2020 Karl T Debiec
#   All rights reserved. This software may be modified and distributed under
#   the terms of the BSD license. See the LICENSE file for details.
"""General-purpose functions not tied to a particular project."""
import logging
from subprocess import PIPE, Popen
from typing import Iterable, Optional


def run_command(
    command: str,
    timeout: int = 600,
    acceptable_exitcodes: Optional[Iterable[int]] = None,
) -> tuple[int, Optional[str], Optional[str]]:
    """Run a provided command.

    Arguments:
        command: command to run
        timeout: maximum time to await command's completion
        acceptable_exitcodes: acceptable exit codes
    Returns:
        exitcode, standard output, and standard error
    Raises:
        ValueError: If exitcode is not one of acceptable_exitcodes
    """
    if acceptable_exitcodes is None:
        acceptable_exitcodes = [0]

    with Popen(command, shell=True, stdout=PIPE, stderr=PIPE) as child:
        exitcode = child.wait(timeout)
        stdout, stderr = child.communicate()
        try:
            stdout = stdout.decode("utf8")
        except UnicodeDecodeError:
            stdout = stdout.decode("ISO-8859-1")
        try:
            stderr = stderr.decode("utf8")
        except UnicodeDecodeError:
            stderr = stderr.decode("ISO-8859-1")
        if exitcode not in acceptable_exitcodes:
            raise ValueError(
                f"subprocess failed with exit code {exitcode};\n\n"
                f"STDOUT:\n"
                f"{stdout}\n\n"
                f"STDERR:\n"
                f"{stderr}"
            )
        return (exitcode, stdout, stderr)


def set_logging_verbosity(verbosity: int) -> None:
    """Set the level of verbosity of logging.

    Arguments:
        verbosity: level of verbosity
    """
    logging.basicConfig()
    if verbosity <= 0:
        logging.getLogger().setLevel(level=logging.ERROR)
    elif verbosity == 1:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif verbosity == 2:
        logging.getLogger().setLevel(level=logging.INFO)
    elif verbosity >= 3:
        logging.getLogger().setLevel(level=logging.DEBUG)
