#  Copyright 2017-2024 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""Testing."""
from __future__ import annotations

import sys
from inspect import getfile
from typing import Type
from unittest.mock import patch

from .command_line_interface import Cli


def run_cli_with_args(cli: Type[Cli], args: str = "") -> None:
    """Run CommandLineInterface as if from shell with provided args.

    Arguments:
        cli: CommandLineInterface to run
        args: Arguments to pass
    """
    with patch.object(sys, "argv", [getfile(cli)] + args.split()):
        cli.main()
