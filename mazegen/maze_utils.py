from typing import List
from mazegen.cell import Cell


def get_neighbors(grid: List[List[Cell]], cell: Cell) -> List[Cell]:
    neighbors = []
    h, w = len(grid), len(grid[0])

    directions = [
        (0, -1),  # N
        (1, 0),   # E
        (0, 1),   # S
        (-1, 0)   # W
    ]

    for dx, dy in directions:
        nx, ny = cell.x + dx, cell.y + dy
        if 0 <= nx < w and 0 <= ny < h:
            neighbor = grid[ny][nx]
            if not neighbor.visited:
                neighbors.append(neighbor)

    return neighbors
