"""
UI layer: User-facing surfaces for the Snake game.

This layer handles rendering to the terminal and capturing user input.
It may import from types, config, service, and runtime.
"""

import curses
import time

from src.config import config
from src.service import SnakeGame
from src.types import GameState


class GameUI:
    def __init__(self, game: SnakeGame):
        self.game = game

    def render(self) -> None:
        state = self.game.get_state()
        height, width = config.BOARD_SIZE
        stdscr = curses.initscr()
        stdscr.clear()
        
        for y in range(height):
            row = []
            for x in range(width):
                pos = Position(x=x, y=y)
                if any(p.x == x and p.y == y for p in state.snake):
                    if Position(x=x, y=y) == state.snake[0]:
                        row.append('X')
                    else:
                        row.append(config.SNAKE_CHAR)
                elif state.food and state.food.x == x and state.food.y == y:
                    row.append(config.FOOD_CHAR)
                else:
                    row.append(config.EMPTY_CHAR)
            stdscr.addstr(y, 0, ''.join(row))
        
        stdscr.addstr(height + 1, 0, f"Score: {state.score}")
        stdscr.refresh()
        curses.endwin()

    def get_input(self) -> Direction | None:
        try:
            key = curses.initscr().getch()
            curses.endwin()
            if key == curses.KEY_UP:
                return Direction.UP
            elif key == curses.KEY_DOWN:
                return Direction.DOWN
            elif key == curses.KEY_LEFT:
                return Direction.LEFT
            elif key == curses.KEY_RIGHT:
                return Direction.RIGHT
            return None
        except:
            return None

    def show_game_over(self, score: int) -> None:
        stdscr = curses.initscr()
        stdscr.clear()
        height, width = config.BOARD_SIZE
        msg = f"Game Over! Score: {score}"
        y = height // 2
        x = (width - len(msg)) // 2
        stdscr.addstr(y, x, msg)
        stdscr.addstr(y + 1, x - 5, "Press any key to exit...")
        stdscr.refresh()
        stdscr.getch()
        curses.endwin()


from src.types import Direction, Position
