#  Copyright 2017-2024 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""General-purpose functions not tied to a particular project."""
from __future__ import annotations

from subprocess import PIPE, Popen
from typing import Iterable


def run_command(
    command: str,
    timeout: int = 600,
    acceptable_exitcodes: Iterable[int] | None = None,
) -> tuple[int, str, str]:
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
            stdout_str = stdout.decode("utf8")
        except UnicodeDecodeError:
            stdout_str = stdout.decode("ISO-8859-1")
        try:
            stderr_str = stderr.decode("utf8")
        except UnicodeDecodeError:
            stderr_str = stderr.decode("ISO-8859-1")
        if exitcode not in acceptable_exitcodes:
            raise ValueError(
                f"subprocess for command:\n"
                f"{command}\n\n"
                f"failed with exit code {exitcode};\n\n"
                f"STDOUT:\n"
                f"{stdout_str}\n\n"
                f"STDERR:\n"
                f"{stderr_str}"
            )

    return exitcode, stdout_str, stderr_str


def run_command_long(command: str) -> tuple[int, str, str]:
    """Run a provided command.

    Arguments:
        command: command to run
    Returns:
        exitcode, standard output, and standard error
    """
    with Popen(command, shell=True, stdout=PIPE, stderr=PIPE) as child:
        stdout, stderr = child.communicate()
        exitcode = child.wait()
        try:
            stdout_str = stdout.decode("utf8")
        except UnicodeDecodeError:
            stdout_str = stdout.decode("ISO-8859-1")
        try:
            stderr_str = stderr.decode("utf8")
        except UnicodeDecodeError:
            stderr_str = stderr.decode("ISO-8859-1")

    return exitcode, stdout_str, stderr_str
