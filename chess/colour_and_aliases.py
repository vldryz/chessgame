"""Enums and Type aliases for the project."""

from __future__ import annotations

from enum import StrEnum

type Square = tuple[int, int]


class Colour(StrEnum):
    """Enum class for piece colours."""

    WHITE = "white"
    BLACK = "black"

    def __invert__(self) -> Colour:
        return Colour.BLACK if self == Colour.WHITE else Colour.WHITE

    def __str__(self) -> str:
        return self.value.title()
