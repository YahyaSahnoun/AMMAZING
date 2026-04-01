from typing import List, Tuple
from mazegen.cell import Cell


def encode_cell(cell: Cell) -> str:
    value: int = 0
    value |= cell.north << 0
    value |= cell.east << 1
    value |= cell.south << 2
    value |= cell.west << 3
    return format(value, "X")


def write_maze_file(
    path: str,
    grid: List[List[Cell]],
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    solution: str
) -> None:
    """
    Writes the maze grid, entry/exit, and solution path to a file.

    Args:
        path (str): Output filename.
        grid (List[List[Cell]]): 2D maze grid.
        entry (Tuple[int,int]): Entry coordinates.
        exit_ (Tuple[int,int]): Exit coordinates.
        solution (str): Path solution string.

    Returns:
        None
    """
    with open(path, "w") as f:
        for row in grid:
            f.write(" ".join(encode_cell(c) for c in row) + "\n")

        f.write(f"\n({entry[0]},{entry[1]})\n")
        f.write(f"({exit_[0]},{exit_[1]})\n")
        f.write(solution + "\n")
