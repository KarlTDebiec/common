#  Copyright 2017-2025 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""Logging utilities."""

from __future__ import annotations

from logging import DEBUG, ERROR, INFO, WARNING, basicConfig, getLogger


def set_logging_verbosity(verbosity: int) -> None:
    """Set the level of verbosity of logging.

    Arguments:
        verbosity: level of verbosity
    """
    basicConfig()
    if verbosity <= 0:
        getLogger().setLevel(level=ERROR)
    elif verbosity == 1:
        getLogger().setLevel(level=WARNING)
    elif verbosity == 2:
        getLogger().setLevel(level=INFO)
    elif verbosity >= 3:
        getLogger().setLevel(level=DEBUG)
