*This project has been created as part of the 42 curriculum by zmajdoub, ysahnoun*

---

# A-Maze-ing 🌀

A Python maze generator that produces perfect or imperfect mazes,
encodes them as hexadecimal wall bitmasks, solves them with BFS, and
renders them in a coloured terminal UI — complete with a hidden "42"
pattern and a reusable pip-installable package.

---

## Description

**A-Maze-ing** generates random mazes of configurable size using the
**recursive backtracker (DFS)** algorithm.  Each cell's four walls
(North, East, South, West) are encoded as a single hex digit.  The
program writes the grid, entry/exit coordinates, and the shortest path
to an output file, then enters an interactive terminal session.

### Why recursive backtracker?

The recursive backtracker (iterative DFS) was chosen because:

- It produces **long, winding corridors** — aesthetically pleasing and
  challenging to solve.
- It runs in **O(W × H)** time and memory — optimal for any maze size.
- It is trivially extended to *imperfect* mazes by randomly removing
  walls after the spanning tree is built.
- The algorithm is well-understood and easy to audit during evaluation.

---

## Instructions

### Requirements

- Python 3.10 or later
- `flake8`, `mypy` (for linting)
- `build` (for the pip package)

### Install dependencies

```bash
make install
# or manually:
pip install flake8 mypy build
```

### Run

```bash
python3 a_maze_ing.py config.txt
# or:
make run
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint          # mandatory flags
make lint-strict   # mypy --strict
```

### Build the pip package

```bash
make build
# Produces: dist/mazegen-1.0.0-py3-none-any.whl
```

### Run tests

```bash
make test
# or: pytest tests/ -v
```

---

## Configuration file format

The config file uses one `KEY=VALUE` pair per line.  Lines starting
with `#` are comments and are ignored.

| Key           | Required | Description                          | Example           |
|---------------|----------|--------------------------------------|-------------------|
| `WIDTH`       | ✅        | Number of columns (≥ 2)              | `WIDTH=20`        |
| `HEIGHT`      | ✅        | Number of rows (≥ 2)                 | `HEIGHT=15`       |
| `ENTRY`       | ✅        | Entry cell as `col,row`              | `ENTRY=0,0`       |
| `EXIT`        | ✅        | Exit cell as `col,row`               | `EXIT=19,14`      |
| `OUTPUT_FILE` | ✅        | Output filename                      | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | ✅        | Perfect maze? (`True`/`False`)       | `PERFECT=True`    |
| `SEED`        | ❌        | Integer RNG seed for reproducibility | `SEED=42`         |
| `ALGORITHM`   | ❌        | Algorithm name (default: `dfs`)      | `ALGORITHM=dfs`   |

---

## Algorithm

**Recursive Backtracker (iterative DFS)**

1. Start with a grid where every cell has all 4 walls closed (mask `0xF`).
2. Stamp the "42" pixel pattern into the grid centre — those cells stay
   at `0xF` and are skipped by the DFS.
3. Pick a starting cell, mark it visited, push it onto a stack.
4. While the stack is non-empty:
   - If the top cell has unvisited neighbours → pick one at random,
     open the shared wall (clear the appropriate bits on both sides),
     push the neighbour.
   - Otherwise → pop the stack (backtrack).
5. For **imperfect** mazes: after the DFS, randomly remove ~15 % of
   interior walls, reverting any removal that would create a 3×3 open
   area.
6. Enforce border walls (all exterior-facing walls set to 1).

---

## Reusable `mazegen` package

### Installation

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Usage

```python
from mazegen import MazeGenerator

# 1. Create and run
gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
gen.generate()

# 2. Access the raw grid (list[list[int]])
grid = gen.grid          # grid[row][col] → 4-bit int

# 3. Solve
path = gen.solve(entry=(0, 0), exit_pos=(19, 14))
print(path)              # "SEESENWWSS..."

# 4. Get hex rows (for the output file)
for line in gen.hex_lines:
    print(line)

# 5. Inspect the "42" pattern cells
print(gen.pattern_42_cells)   # set of (col, row) tuples
```

### Custom parameters

| Parameter | Type    | Default | Description                        |
|-----------|---------|---------|------------------------------------|
| `width`   | `int`   | 20      | Number of columns (≥ 2)            |
| `height`  | `int`   | 15      | Number of rows (≥ 2)               |
| `seed`    | `int?`  | `None`  | RNG seed (`None` = random)         |
| `perfect` | `bool`  | `True`  | Perfect maze (unique path) or not  |

The grid format and the output file format are **independent**: the
grid stores raw bitmask integers; the output file encodes them as hex
characters.

---

## What part of the code is reusable

The `mazegen/` directory is a standalone, dependency-free Python
package:

- `mazegen/generator.py` — `MazeGenerator` class (full DFS engine,
  42-pattern, border enforcement, BFS solver, hex export).
- `mazegen/__init__.py` — public API (`from mazegen import MazeGenerator`).

Build with `make build`; install with `pip install dist/*.whl`.

---

## Team and project management

### Roles

| Person   | Area                      | Files                                              |
|----------|---------------------------|----------------------------------------------------|
| Person 1 | Algorithm / Maze Engine   | `cell.py`, `maze_generator.py`, `pathfinder.py`, `maze_utils.py`, `mazegen/` |
| Person 2 | Application / Interface   | `a_maze_ing.py`, `config_parser.py`, `file_writer.py`, `renderer.py`, `interaction.py` |

### Planning

| Week | Goal                                         | Outcome                   |
|------|----------------------------------------------|---------------------------|
| 1    | DFS engine + Cell + pathfinder               | ✅ Done on schedule        |
| 1    | Config parser + file writer                  | ✅ Done on schedule        |
| 2    | 42 pattern + border enforcement              | ✅ Minor tuning needed     |
| 2    | Renderer + colour themes + interaction loop  | ✅ Completed               |
| 2    | pip package + Makefile + README + tests      | ✅ Completed               |

**What worked well:** separating the algorithm from the I/O layer from
the start meant zero merge conflicts and easy parallel development.

**What could be improved:** the 3×3 open-area check for imperfect mazes
could be made more efficient with a precomputed region tracking structure.

**Tools used:** VS Code, Git, pytest, mypy, flake8, Python `build`.

---

## Resources

- [Maze Generation Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Graph Theory & Spanning Trees — MIT OpenCourseWare](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/)
- [Python `typing` module — docs.python.org](https://docs.python.org/3/library/typing.html)
- [ANSI Escape Codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)

### AI usage

Claude (Anthropic) was used to:
- Suggest the structure for the interactive menu loop (`interaction.py`).
- Generate the initial docstring templates (all reviewed and edited).
- Brainstorm the 42-pixel-art bitmask layout.

All generated content was reviewed, tested, and understood by the team
before inclusion.  No code was blindly copy-pasted.