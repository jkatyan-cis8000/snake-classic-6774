# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types/__init__.py: Type definitions for Direction, Position, GameState, Difficulty
- src/types/food.py: Food placement logic (parse only, no validation logic)
- src/config/__init__.py: Constants: BOARD_SIZE, SNAKE_CHAR, FOOD_CHAR, EMPTY_CHAR
- src/config/difficulty.py: Speed settings for EASY, NORMAL, HARD levels
- src/service/__init__.py: SnakeGame class with core game logic
- src/service/snake.py: Snake state and movement logic
- src/ui/__init__.py: GameUI class for rendering and input
- src/runtime/__init__.py: Main entry point (main, run_game), game loop orchestration

## Interfaces

### types module
- `Direction` enum: UP, DOWN, LEFT, RIGHT
- `Position` dataclass: x: int, y: int
- `Difficulty` enum: EASY, NORMAL, HARD
- `GameState` dataclass: snake: list[Position], food: Position | None, direction: Direction, score: int, game_over: bool, difficulty: Difficulty

### config module
- BOARD_SIZE: tuple[int, int] = (20, 20)
- SNAKE_CHAR: str = 'O'
- FOOD_CHAR: str = '*'
- EMPTY_CHAR: str = '.'
- SPEEDS: dict[Difficulty, float] = {EASY: 0.2, NORMAL: 0.1, HARD: 0.05}

### service module
- `SnakeGame.__init__(difficulty: Difficulty = Difficulty.NORMAL)`: Initialize game
- `SnakeGame.move(direction: Direction) -> None`: Move snake in direction
- `SnakeGame.get_state() -> GameState`: Return current game state
- `SnakeGame.is_valid_direction(new_dir: Direction) -> bool`: Check if direction change is valid
- `SnakeGame.reset() -> None`: Reset game to start state

### ui module
- `GameUI.__init__(game: SnakeGame)`: Initialize UI with game instance
- `GameUI.render() -> None`: Render current game state to terminal
- `GameUI.get_input() -> Direction | None`: Get next input, returns None if no input
- `GameUI.show_game_over(score: int) -> None`: Display game over screen

### runtime module
- `main() -> None`: Entry point, runs game loop
- `run_game(difficulty: Difficulty) -> None`: Run a single game session

## Shared Data Structures

```python
# Position
@dataclass
class Position:
    x: int  # column index
    y: int  # row index

# GameState
@dataclass
class GameState:
    snake: list[Position]        # Head is first element
    food: Position | None        # Current food location
    direction: Direction         # Current movement direction
    score: int                   # Food eaten count
    game_over: bool              # Game end state
    difficulty: Difficulty       # Current difficulty level
```

## External Dependencies

- Python standard library only: `curses` for terminal UI, `time` for game loop, `enum` for types, `dataclasses` for state

## Implementation Status

All modules have been implemented and verified:
- **types** (Direction, Position, GameState, Difficulty, Food): Complete
- **config** (BOARD_SIZE, chars, SPEEDS): Complete
- **service** (SnakeGame class): Complete
- **ui** (GameUI class): Complete
- **runtime** (main, run_game): Complete

Lint passes with no violations. The Snake game is ready for use.
