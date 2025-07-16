# Copyright 2017-2025 Karl T Debiec. All rights reserved. This software may be modified
# and distributed under the terms of the BSD license. See the LICENSE file for details.
"""Tests for :mod:`common.validation`."""

from __future__ import annotations

import pytest  # type: ignore
from common.validation import validate_ints  # type: ignore


def test_validate_ints_length_error() -> None:
    """Validate that length mismatch error references length."""
    with pytest.raises(ValueError) as excinfo:
        validate_ints([1, 2], length=3)

    assert str(excinfo.value) == "'[1, 2]' is of length 2, not '3'"
