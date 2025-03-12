#  Copyright 2017-2025 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""General-purpose functions not tied to a particular project."""
from __future__ import annotations

import threading
from collections.abc import Iterable


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


from subprocess import PIPE, Popen


def run_command_live(
    command: str,
    timeout: int | None = 600,
    acceptable_exitcodes: Iterable[int] | None = None,
) -> tuple[int, str, str]:
    """Run a provided command and stream output live.

    Arguments:
        command: Command to run
        timeout: Maximum time to await command's completion
        acceptable_exitcodes: Acceptable exit codes
    Returns:
        exitcode, standard output, and standard error
    Raises:
        ValueError: If exitcode is not one of acceptable_exitcodes
    """
    if acceptable_exitcodes is None:
        acceptable_exitcodes = [0]

    stdout_lines = []
    stderr_lines = []

    def read_stream(stream, lines):
        for line in iter(stream.readline, ""):
            print(line, end="")
            lines.append(line)
        stream.close()

    with Popen(
        command,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        bufsize=0,
        encoding="utf-8",
    ) as child:
        stdout_thread = threading.Thread(
            target=read_stream, args=(child.stdout, stdout_lines)
        )
        stderr_thread = threading.Thread(
            target=read_stream, args=(child.stderr, stderr_lines)
        )

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join(timeout)
        stderr_thread.join(timeout)

        exitcode = child.wait(timeout)

        stdout_str = "".join(stdout_lines)
        stderr_str = "".join(stderr_lines)

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
