"""
Service layer: Business logic for the Snake game.

This layer contains the core game rules: movement, collision detection,
eating food, and game state management. It may import from types, config,
and providers.
"""

import random

from src.config import config, SPEEDS
from src.service.snake import Snake
from src.types import Direction, Difficulty, GameState, Position, generate_food


class SnakeGame:
    def __init__(self, difficulty: Difficulty = Difficulty.NORMAL):
        self.snake = Snake()
        self.food = generate_food(self.snake.get_positions())
        self.direction = Direction.RIGHT
        self.score = 0
        self.game_over = False
        self.difficulty = difficulty
        self.speed = SPEEDS[difficulty]

    def move(self, direction: Direction) -> None:
        if self.game_over:
            return
        if not self.is_valid_direction(direction):
            direction = self.direction
        self.snake.move(direction)
        self.direction = direction
        if self.snake.check_collision():
            self.game_over = True
            return
        if self.food and self.snake.head() == self.food:
            self.snake.grow()
            self.score += 1
            self.food = generate_food(self.snake.get_positions())

    def is_valid_direction(self, new_dir: Direction) -> bool:
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites.get(new_dir) != self.direction

    def get_state(self) -> GameState:
        return GameState(
            snake=self.snake.get_positions(),
            food=self.food,
            direction=self.direction,
            score=self.score,
            game_over=self.game_over,
            difficulty=self.difficulty,
        )

    def reset(self) -> None:
        self.snake.reset()
        self.food = generate_food(self.snake.get_positions())
        self.direction = Direction.RIGHT
        self.score = 0
        self.game_over = False
