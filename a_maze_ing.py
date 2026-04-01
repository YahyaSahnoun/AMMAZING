import sys
from typing import Dict, Any

from mazegen.config_parser import parse_config
from mazegen.maze_generator import MazeGenerator
from mazegen.pathfinder import find_shortest_path
from mazegen.file_writer import write_maze_file

from mazegen.interaction import get_key, clear
from mazegen.renderer import draw_maze
import mazegen.renderer as renderer


def interactive_mode(generator: MazeGenerator, config: Dict[str, Any]) -> None:
    grid = generator.generate_maze()

    show_path: bool = False
    path: str = ""

    small_grid_warning: bool = False
    if config["width"] < 12 or config["height"] < 12:
        small_grid_warning = True

    while True:
        clear()

        if show_path:
            path = find_shortest_path(grid, config["entry"], config["exit"])

        draw_maze(
            grid,
            path=path if show_path else None,
            entry=config["entry"],
            exit_=config["exit"],
            pattern_42=generator.pattern_42
        )
        if small_grid_warning:
            print("\n Grid too small to draw the 42 pattern!")
            print(" Minimum size to draw the 42 pattern is 12x12.\n")

        print("\n[R] regenerate | [P] toggle path | [C] color | [Q] quit")

        key: str = get_key()

        if key.lower() == "r":
            generator = MazeGenerator(
                width=config["width"],
                height=config["height"],
                perfect=config["perfect"],
                seed=config.get("seed")
            )
            grid = generator.generate_maze()

        elif key.lower() == "p":
            show_path = not show_path

        elif key.lower() == "c":
            renderer.current_theme = (renderer.current_theme + 1) % len(
                renderer.THEMES)

        elif key.lower() == "q":
            break


def main() -> None:
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py config.txt")
            return

        config: Dict[str, Any] = parse_config(sys.argv[1])

        generator = MazeGenerator(
            config["width"],
            config["height"],
            perfect=config["perfect"],
            seed=config.get("seed")
        )

        generator.entry_override = config["entry"]
        generator.exit_override = config["exit"]

        grid = generator.generate_maze()

        path: str = find_shortest_path(
            grid,
            config["entry"],
            config["exit"]
        )

        write_maze_file(
            config["output"],
            grid,
            config["entry"],
            config["exit"],
            path
        )

        interactive_mode(generator, config)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
