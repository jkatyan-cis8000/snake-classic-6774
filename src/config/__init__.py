"""
Config layer: Constants and settings for the Snake game.

This layer holds configuration values like board dimensions, display
characters, and difficulty settings. It may import only from types.
"""

from dataclasses import dataclass

from src.types import Difficulty


@dataclass
class Config:
    BOARD_SIZE: tuple[int, int] = (20, 20)
    SNAKE_CHAR: str = 'O'
    FOOD_CHAR: str = '*'
    EMPTY_CHAR: str = '.'


SPEEDS: dict[Difficulty, float] = {
    Difficulty.EASY: 0.2,
    Difficulty.NORMAL: 0.1,
    Difficulty.HARD: 0.05,
}

config = Config()
