#  Copyright 2017-2025 Karl T Debiec. All rights reserved. This software may be modified
#  and distributed under the terms of the BSD license. See the LICENSE file for details.
"""Typing."""
from __future__ import annotations

from pathlib import Path
from typing import TypeAlias

PathLike: TypeAlias = Path | str
