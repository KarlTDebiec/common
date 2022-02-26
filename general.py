#!/usr/bin/env python
#   common/general.py
#
#   Copyright (C) 2017-2020 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""General-purpose functions not tied to a particular project."""
from subprocess import PIPE, Popen
from typing import Iterable, Optional, Tuple


def get_shell_type() -> Optional[str]:
    """
    Determines if inside IPython prompt.

    Returns:
        Type of shell in use, or None if not in a shell
    """
    try:
        # noinspection Mypy
        shell = str(get_ipython().__class__.__name__)
        if shell == "ZMQInteractiveShell":
            # IPython in Jupyter Notebook
            return shell
        if shell == "InteractiveShellEmbed":
            # IPython in Jupyter Notebook using IPython.embed
            return shell
        if shell == "TerminalInteractiveShell":
            # IPython in terminal
            return shell
        # Other
        return shell
    except NameError:
        # Not in IPython
        return None


def run_command(
    command: str,
    timeout: int = 600,
    acceptable_exitcodes: Optional[Iterable[int]] = None,
) -> Tuple[int, Optional[str], Optional[str]]:
    """

    Arguments:
        command: command to run
        timeout: maximum time to await command's completion
        acceptable_exitcodes: acceptable exit codes
    Returns:
        exitcode, standard output, and standard error
    Raises:
        ValueError: If exitcode is not in acceptable_exitcodes
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
