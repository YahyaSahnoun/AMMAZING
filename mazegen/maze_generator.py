import random
from typing import List, Set, Tuple, Optional
from mazegen.cell import Cell
from mazegen.maze_utils import get_neighbors


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = True,
        seed: Optional[int] = None
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.perfect: bool = perfect
        self.seed: Optional[int] = seed
        if seed is not None:
            random.seed(str(seed))

        self.grid: List[List[Cell]] = self.create_grid()
        self.pattern_42: Set[Tuple[int, int]] = set()

        # Optional overrides
        self.entry_override: Optional[Tuple[int, int]] = None
        self.exit_override: Optional[Tuple[int, int]] = None

    def create_grid(self) -> List[List[Cell]]:
        return [[Cell(x, y) for x in range(self.width)] for y in range(
            self.height)]

    def init_42_pattern(self) -> None:
        if self.width < 12 or self.height < 12:
            print(f"Grid too small ({self.width}x{self.height})",
                  "– skipping 42 pattern")
            return

        cx, cy = self.width // 2, self.height // 2

        pattern: List[str] = [
            "01000111 ",
            "01000  1 ",
            "01110111 ",
            "000101   ",
            "00010111 ",
        ]

        start_x = cx - 5
        start_y = cy - 2

        for dy, row in enumerate(pattern):
            for dx, val in enumerate(row):
                if val == "1":
                    x = start_x + dx
                    y = start_y + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.pattern_42.add((x, y))
                        self.grid[y][x].passable = False

    def generate_maze(self) -> List[List[Cell]]:
        if self.seed is not None:
            random.seed(str(self.seed))

        self.init_42_pattern()

        for row in self.grid:
            for cell in row:
                cell.visited = False
                cell.north = cell.south = cell.east = cell.west = True
                # if not hasattr(cell, "passable"):
                #     cell.passable = True

        entry: Tuple[int, int] = (0, 0)
        exit_: Tuple[int, int] = (self.width - 1, self.height - 1)
        if self.entry_override is not None:
            entry = self.entry_override
        if self.exit_override is not None:
            exit_ = self.exit_override

        if entry in self.pattern_42:
            raise ValueError("This ENTRY is inside the 42 pattern!")
        if exit_ in self.pattern_42:
            raise ValueError("This EXIT is inside the 42 pattern!")

        stack: List[Cell] = []

        current: Cell = self.grid[0][0]
        if not current.passable:
            raise ValueError("Start is inside blocked 42 pattern")

        current.visited = True

        while True:
            neighbors: List[Cell] = [
                n for n in get_neighbors(self.grid, current
                                         ) if n.passable and not n.visited
            ]

            if neighbors:
                nxt: Cell = random.choice(neighbors)
                current.remove_wall(nxt)
                stack.append(current)
                nxt.visited = True
                current = nxt
            elif stack:
                current = stack.pop()
            else:
                break

        if not self.perfect:
            self._add_loops()

        return self.grid

    # ───────────── Safety check helpers ─────────────
    def _has_large_open_zone(self, size: int = 3) -> bool:
        """Return True if there is any size x size open block ."""
        h, w = self.height, self.width
        for y in range(h - size + 1):
            for x in range(w - size + 1):
                all_open = True
                for dy in range(size):
                    for dx in range(size):
                        cell = self.grid[y + dy][x + dx]
                        if cell.north or cell.south or cell.east or cell.west:
                            all_open = False
                            break
                    if not all_open:
                        break
                if all_open:
                    return True
        return False

    def _can_remove_wall_safely(self, cell1: Cell, cell2: Cell) -> bool:
        """Check if removing the wall would create a large open zone."""
        # Temporarily remove wall
        walls_before = (cell1.north, cell1.east, cell1.south, cell1.west,
                        cell2.north, cell2.east, cell2.south, cell2.west)
        cell1.remove_wall(cell2)
        too_open = self._has_large_open_zone()
        # Restore walls
        (cell1.north, cell1.east, cell1.south, cell1.west,
         cell2.north, cell2.east, cell2.south, cell2.west) = walls_before
        return not too_open

    # ───────────── Add loops safely ─────────────
    def _add_loops(self) -> None:
        for _ in range((self.width * self.height) // 10):
            x: int = random.randint(0, self.width - 2)
            y: int = random.randint(0, self.height - 2)

            cell: Cell = self.grid[y][x]
            neighbor: Cell = self.grid[y][x + 1]

            if cell.passable and neighbor.passable:
                if self._can_remove_wall_safely(cell, neighbor):
                    cell.remove_wall(neighbor)

    def validate_maze(self) -> bool:
        return True
