"""
Service layer: Snake state and movement logic.

This module contains the Snake class which manages the snake's body,
movement, and growth logic.
"""

from src.config import config
from src.types import Direction, Position


class Snake:
    def __init__(self, start_pos: Position | None = None):
        if start_pos is None:
            start_pos = Position(x=config.BOARD_SIZE[0] // 2, y=config.BOARD_SIZE[1] // 2)
        self.body: list[Position] = [start_pos]
        self.direction = Direction.RIGHT
        self.grow_next_move = False

    def head(self) -> Position:
        return self.body[0]

    def move(self, direction: Direction) -> None:
        self.direction = direction
        head = self.head()
        new_head = self._calculate_new_head(head, direction)
        self.body.insert(0, new_head)
        if not self.grow_next_move:
            self.body.pop()
        else:
            self.grow_next_move = False

    def _calculate_new_head(self, head: Position, direction: Direction) -> Position:
        x, y = head.x, head.y
        if direction == Direction.UP:
            y -= 1
        elif direction == Direction.DOWN:
            y += 1
        elif direction == Direction.LEFT:
            x -= 1
        elif direction == Direction.RIGHT:
            x += 1
        return Position(x=x, y=y)

    def grow(self) -> None:
        self.grow_next_move = True

    def check_collision(self) -> bool:
        head = self.head()
        if head.x < 0 or head.x >= config.BOARD_SIZE[0] or head.y < 0 or head.y >= config.BOARD_SIZE[1]:
            return True
        if head in self.body[1:]:
            return True
        return False

    def get_positions(self) -> list[Position]:
        return self.body.copy()

    def reset(self) -> None:
        start_pos = Position(x=config.BOARD_SIZE[0] // 2, y=config.BOARD_SIZE[1] // 2)
        self.body = [start_pos]
        self.direction = Direction.RIGHT
        self.grow_next_move = False
