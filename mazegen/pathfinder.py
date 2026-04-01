from collections import deque
from typing import List, Tuple, Dict
from mazegen.cell import Cell


DIRECTIONS: Dict[str, Tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}


def find_shortest_path(
    grid: List[List[Cell]],
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> str:
    queue: deque[Tuple[int, int]] = deque([start])
    visited: set[Tuple[int, int]] = set([start])
    parent: Dict[Tuple[int, int], Tuple[int, int, str]] = {}

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            return reconstruct_path(parent, start, end)

        cell: Cell = grid[y][x]

        for d, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy

            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                continue

            if (nx, ny) in visited:
                continue

            if not grid[ny][nx].passable:
                continue

            if (
                (d == "N" and cell.north) or
                (d == "E" and cell.east) or
                (d == "S" and cell.south) or
                (d == "W" and cell.west) or
                (not grid[ny][nx].passable)  # skip obstacles
            ):
                continue

            visited.add((nx, ny))
            parent[(nx, ny)] = (x, y, d)
            queue.append((nx, ny))

    return ""


def reconstruct_path(
    parent: Dict[Tuple[int, int], Tuple[int, int, str]],
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> str:
    path: List[str] = []
    current: Tuple[int, int] = end

    while current != start:
        px, py, d = parent[current]
        path.append(d)
        current = (px, py)

    return "".join(reversed(path))
