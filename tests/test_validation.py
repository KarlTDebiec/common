#  Copyright 2017-2025 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""Tests for :mod:`common.validation`."""

from __future__ import annotations

# pyright: reportMissingImports=false
import pytest

from common.validation import validate_float, validate_int


def test_validate_float_error_message() -> None:
    """Value with invalid float type raises correct message."""
    with pytest.raises(TypeError, match="cannot be cast to float"):
        validate_float("abc")


def test_validate_int_error_message() -> None:
    """Value with invalid int type raises correct message."""
    with pytest.raises(TypeError, match="cannot be cast to int"):
        validate_int("abc")
