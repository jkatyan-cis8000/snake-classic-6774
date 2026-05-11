"""
Runtime layer: Application lifecycle and orchestration.

This layer handles the main game loop, event handling, and wiring together
components. It may import from types, config, service, and providers.
"""
import curses
import time

from src.config import SPEEDS
from src.service import SnakeGame
from src.types import Difficulty, Direction, Position


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


def run_game(difficulty: Difficulty) -> None:
    game = SnakeGame(difficulty=difficulty)
    ui = GameUI(game)

    while not game.get_state().game_over:
        ui.render()
        direction = ui.get_input()
        if direction:
            game.move(direction)
        time.sleep(SPEEDS[difficulty])

    ui.show_game_over(game.get_state().score)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description='Snake Game')
    parser.add_argument('--difficulty', choices=['easy', 'normal', 'hard'],
                        default='normal', help='Game difficulty level')
    args = parser.parse_args()

    difficulty_map = {
        'easy': Difficulty.EASY,
        'normal': Difficulty.NORMAL,
        'hard': Difficulty.HARD,
    }

    run_game(difficulty_map[args.difficulty])
