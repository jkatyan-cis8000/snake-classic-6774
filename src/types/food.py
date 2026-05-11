"""
Types layer: Food placement logic for the Snake game.

This module handles food generation and placement on the board.
"""

import random

from src.config import config
from src.types import Position


def generate_food(snake_positions: list[Position]) -> Position | None:
    """Generate food at a random position not occupied by the snake."""
    occupied = set((p.x, p.y) for p in snake_positions)
    available = []
    for x in range(config.BOARD_SIZE[0]):
        for y in range(config.BOARD_SIZE[1]):
            if (x, y) not in occupied:
                available.append(Position(x=x, y=y))
    if not available:
        return None
    return random.choice(available)
