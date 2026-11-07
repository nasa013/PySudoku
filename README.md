# PySudoku — Interactive Sudoku Engine & Solver

An object-oriented Sudoku engine written in **pure Python 3.10+ (standard library only)**.
It reads puzzles from text files, checks that they follow the rules, solves them with a
**hand-written backtracking algorithm**, reports whether the solution is unique, and grades a
player's submitted answer cell by cell.

No third-party packages are used anywhere. There is nothing to install, and `requirements.txt`
(if present) is empty.

## Features

| Mode | Command | What it does |
| --- | --- | --- |
| Solve | `python -m pysudoku solve --file data/puzzle.txt` | Validates the board, solves it, and says whether it has 0, 1 or several solutions |
| Verify | `python -m pysudoku verify --puzzle data/puzzle.txt --submission data/player_submission.txt` | Compares a player's grid with the puzzle and lists every mistake |
| Generate (bonus) | `python -m pysudoku generate --level easy --out data/new.txt` | Creates a new puzzle with a unique solution |
| Play (bonus) | `python -m pysudoku play --file data/easy_puzzle.txt` | Interactive game in the terminal |

## Requirements

- Python **3.10 or newer**
- Nothing else. No `pip install`.

Check your version:

```bash
python --version
```

## Project layout

```
pysudoku-project/
├── pysudoku/
│   ├── __init__.py        # exports Board, Solver, Verifier
│   ├── __main__.py        # makes `python -m pysudoku` work; calls cli.main()
│   ├── board.py           # Board: parsing, validation, printing
│   ├── solver.py          # Solver: backtracking, count_solutions
│   ├── verifier.py        # Verifier + VerificationReport
│   ├── exceptions.py      # SudokuError and subclasses
│   └── cli.py             # argparse subcommands, all console output
├── tests/
│   ├── test_board.py
│   ├── test_solver.py
│   ├── test_verifier.py
│   └── data/              # one board per test case
├── data/
│   ├── puzzle.txt
│   ├── player_submission.txt
│   ├── multiple_solutions.txt
│   └── unsolvable.txt
└── README.md
```

Each class has one job:

- **`Board`** holds the 9×9 grid, remembers which cells were given, parses files, finds rule conflicts, and prints the grid with dividers.
- **`Solver`** runs the backtracking search on a **copy** of the board. It never changes the board it was given.
- **`Verifier`** compares a player's grid with the original puzzle and returns a `VerificationReport`.
- **`cli.py`** is the only file that prints. Everything else returns data.

## Running the program

**Always run commands from the project root** (the folder that contains `pysudoku/`), using `python -m`.

### Solve

```bash
python -m pysudoku solve --file data/puzzle.txt
```

Example output:

```
[+] Loading puzzle from: data/puzzle.txt
[+] Validating board configuration... OK
[+] Running Sudoku solver...

=== SOLUTION FOUND ===
5 3 4 | 6 7 8 | 9 1 2
...

[+] Solution analysis: UNIQUE SOLUTION (exactly 1 solution exists).
```

The analysis line is one of:

| Result | Meaning |
| --- | --- |
| `NO SOLUTION` | The clues contradict each other |
| `UNIQUE SOLUTION` | A proper Sudoku puzzle |
| `MULTIPLE SOLUTIONS` | The puzzle is ambiguous (one solution is shown) |

If the starting board repeats a digit in a row, column or box, the program stops before solving and lists every conflict.

### Verify

```bash
python -m pysudoku verify --puzzle data/puzzle.txt --submission data/player_submission.txt
```

Problems are reported in this order:

1. **Given cells changed:** a clue from the puzzle has a different value in the submission.
2. **Empty cells:** any `0` or `.` left in the submission.
3. **Duplicates:** a digit repeated in a row, column or box.

Final status:

| Status | Meaning |
| --- | --- |
| `VALID SOLUTION` | No problems at all |
| `INCOMPLETE` | Only empty cells, and no rule is broken so far |
| `INVALID SOLUTION` | At least one changed given or duplicate |

Rows and columns are **1-based** in every message, because players count from 1.

### Speed report (bonus)

```bash
python -m pysudoku solve --file data/puzzle.txt --stats
```

Prints the number of recursive calls and the time taken (`time.perf_counter`).

### Generate (bonus)

```bash
python -m pysudoku generate --level medium --out data/new.txt --seed 42
```

- `--level easy|medium|hard` keeps about 40, 32 or 26 given cells.
- `--seed` makes a run repeatable.

### Play (bonus)

```bash
python -m pysudoku play --file data/easy_puzzle.txt
```

On Windows this is a plain text loop with ANSI colors. Commands are typed as `row column value`, for example `5 3 7` puts 7 at row 5, column 3.

### Help

```bash
python -m pysudoku --help
python -m pysudoku solve --help
```

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Success |
| `1` | Invalid or unsolvable board, or a failed verification |
| `2` | Bad arguments or a missing file |

## Input file format

Puzzle and submission files use the same format.

- Empty cells are `0` or `.`.
- Digits may be separated by spaces or not: `530070000` and `5 3 0 0 7 0 0 0 0` are the same row.
- The characters `|`, `-` and `+` are ignored anywhere, and lines made only of them are skipped.
- Blank lines and lines starting with `#` are ignored.
- After cleaning, there must be exactly **9 rows of 9 cells**.
- Any other character (a letter, `10`, `*`) is an error.

Both of these files describe the same puzzle:

```
# Sample puzzle (0 = empty)
5 3 0 | 0 7 0 | 0 0 0
6 0 0 | 1 9 5 | 0 0 0
0 9 8 | 0 0 0 | 0 6 0
------+-------+------
8 0 0 | 0 6 0 | 0 0 3
4 0 0 | 8 0 3 | 0 0 1
7 0 0 | 0 2 0 | 0 0 6
------+-------+------
0 6 0 | 0 0 0 | 2 8 0
0 0 0 | 4 1 9 | 0 0 5
0 0 0 | 0 8 0 | 0 7 9
```

```
53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79
```

Malformed files raise `InvalidBoardFormatError` with the row number and what was found, for example `Row 4 has 8 cells, expected 9`.

## Errors

| Exception | When |
| --- | --- |
| `SudokuError` | Base class for all PySudoku errors |
| `InvalidBoardFormatError` | The file content is malformed (wrong shape or bad characters) |
| `InvalidBoardError` | The starting board repeats a digit in a row, column or box (carries the list of conflicts) |

A missing file stays Python's own `FileNotFoundError` and is handled in `cli.py`.

## How the solver works

The solver uses **backtracking**: find an empty cell, try each digit 1–9 that does not clash with its row, column or box, place it, and recurse. If the recursion fails, the cell is reset to `0` and the next digit is tried. If no digit works, the call returns failure to its caller, which undoes its own choice. This is the "pencil and eraser" way of solving a Sudoku.

The solver works on a **copy** of the board, so the original puzzle object is never changed.

### How `count_solutions` stops early

`Solver.count_solutions(limit=2)` runs the same backtracking search, but when it reaches a full board it does not stop. It adds one to a counter, then undoes its last choice and keeps searching for other solutions. As soon as the counter reaches `limit` (2 by default), the search returns `True` all the way up the call stack and everything stops at once. Two solutions are enough to say "multiple solutions", so the solver never counts them all. This matters because an empty board has about 6.7 × 10²¹ solutions, and stopping at 2 is what lets it finish in well under a second.

| `count_solutions()` returns | Report |
| --- | --- |
| `0` | `NO SOLUTION` |
| `1` | `UNIQUE SOLUTION` |
| `2` | `MULTIPLE SOLUTIONS` |

### Speed-ups

- **Constraint sets:** three lists of sets (`rows`, `cols`, `boxes`) make a clash check `O(1)` instead of scanning 27 cells.
- **MRV heuristic:** the solver picks the empty cell with the **fewest** legal candidates first, which cuts the search tree.

### MRV comparison

Measured with `--stats` on the same board:

| Board | Recursive calls without MRV | Recursive calls with MRV |
| --- | --- | --- |
| `data/puzzle.txt` | _fill in after running_ | _fill in after running_ |

## Running the tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

Tests cover parsing, validation, solving, uniqueness, and verification. Each test board lives in its own file under `tests/data/`.
