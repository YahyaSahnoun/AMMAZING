from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    visited: bool = False
    passable: bool = True

    def remove_wall(self, other: "Cell") -> None:
        dx = other.x - self.x
        dy = other.y - self.y

        if dx == 1:
            self.east = False
            other.west = False
        elif dx == -1:
            self.west = False
            other.east = False
        elif dy == 1:
            self.south = False
            other.north = False
        elif dy == -1:
            self.north = False
            other.south = False
