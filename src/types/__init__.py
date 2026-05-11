"""
Types layer: Pure type definitions for the Snake game.

No logic or computation belongs here — only data structures and enums
that represent game concepts.
"""
from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


@dataclass
class Position:
    x: int
    y: int


class Difficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3


@dataclass
class GameState:
    snake: list[Position]
    food: Position | None
    direction: Direction
    score: int
    game_over: bool
    difficulty: Difficulty
