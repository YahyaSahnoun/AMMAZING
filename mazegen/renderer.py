from typing import Optional, Sequence, Tuple, Set
from colorama import init
from mazegen.cell import Cell

init()

# ───────────── Themes ─────────────
THEMES: list[dict[str, str]] = [
    {"wall": "\033[37m", "path": "\033[32m", "entry": "\033[34m",
     "exit": "\033[31m"},
    {"wall": "\033[36m", "path": "\033[33m", "entry": "\033[35m",
     "exit": "\033[31m"},
    {"wall": "\033[90m", "path": "\033[92m", "entry": "\033[94m",
     "exit": "\033[91m"},
]

RESET: str = "\033[0m"
current_theme: int = 0


# ───────────── Functions ─────────────
def get_colors() -> dict[str, str]:
    """Return the currently selected theme colors."""
    return THEMES[current_theme]


def draw_maze(
    grid: list[list[Cell]],
    path: Optional[Sequence[str]] = None,
    entry: Optional[Tuple[int, int]] = None,
    exit_: Optional[Tuple[int, int]] = None,
    pattern_42: Optional[Set[Tuple[int, int]]] = None,
) -> None:
    """
    Render the maze in the terminal with optional path, entry/exit

    Args:
        grid: 2D list of Cell objects representing the maze.
        path: Sequence of moves ("N", "S", "E", "W") for the solution path.
        entry: Coordinates (x, y) of the maze entry.
        exit_: Coordinates (x, y) of the maze exit.
        pattern_42: Set of coordinates for special pattern cells.
    """
    colors: dict[str, str] = get_colors()
    WALL: str = colors["wall"]
    ENTRY: str = colors["entry"]
    EXIT: str = colors["exit"]

    h: int = len(grid)
    w: int = len(grid[0])

    gradient: list[str] = ["\033[92m", "\033[93m", "\033[91m"]
    path_positions: list[Tuple[int, int]] = []
    path_set: Set[Tuple[int, int]] = set()

    if path and entry:
        x, y = entry
        path_positions.append((x, y))
        for move in path:
            if move == "N":
                y -= 1
            elif move == "S":
                y += 1
            elif move == "E":
                x += 1
            elif move == "W":
                x -= 1
            path_positions.append((x, y))
        path_set = set(path_positions)

    for y in range(h):
        top: str = ""
        middle: str = ""
        for x in range(w):
            cell: Cell = grid[y][x]

            # ───── TOP WALL
            top += "┼───" if cell.north else "┼   "

            # ───── LEFT WALL
            middle += "│" if cell.west else " "

            # ───── CELL CONTENT
            if entry and (x, y) == entry:
                middle += ENTRY + " 🐵" + RESET
            elif exit_ and (x, y) == exit_:
                middle += EXIT + " 🍌" + RESET
            elif pattern_42 and (x, y) in pattern_42:
                middle += "\033[95m" + "▓▒▓" + RESET
            elif (x, y) in path_set:
                idx: int = path_positions.index((x, y))
                color: str = gradient[idx % len(gradient)]
                middle += color + " • " + RESET
            else:
                middle += "   "

        print(WALL + top + "┼" + RESET)
        print(WALL + middle + "│" + RESET)

    # Bottom line
    print(WALL + "┼───" * w + "┼" + RESET)
