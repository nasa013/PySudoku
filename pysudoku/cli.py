import argparse
from .board import Board
from .exceptions import InvalidBoardFormatError
from .solver import Solver
from .verifier import Verifier


def build_parser() -> argparse.ArgumentParser:

    """
    Create the command-line parser with the subcommands solve and verify
    """
    parser = argparse.ArgumentParser(prog="pysudoku", description="Sudoku engine and solver")
    sub = parser.add_subparsers(dest="command", required=True)

    solve = sub.add_parser("solve", help="Solve a puzzle and check uniqueness")

    solve.add_argument("--file", required=True, help="Path to the puzzle file")

    verify= sub.add_parser("verify", help= "verify the puzzle" )
    verify.add_argument("--puzzle", required=True, help="Path to the original puzzle file")
    verify.add_argument("--submission", required=True, help="Path to the player's submission file")


    return parser

def cmd_solve(args) -> int:
    """
    Load and validate a puzzle (solving comes next). 
    Return the exit code
    """
    print(f"[+] Loading puzzle from: {args.file}")

    try: # load
        board = Board.from_file(args.file)
    except FileNotFoundError:
        print(f"[!] File not found: {args.file}")
        return 2
    except InvalidBoardFormatError as e:
        print(f"[!] {e}")
        return 1

    print("[+] Validating board configuration... ", end="")
    conflicts = board.find_conflicts()
    if conflicts:
        print("FAILED")
        for message in conflicts:
            print(f"[!] {message}")
        return 1
    print("OK")

    print("[+] Running Sudoku solver...")
    solver = Solver(board)
    count = solver.count_solutions()

    if count == 0:
        print()
        print("[+] Solution analysis: NO SOLUTION (the clues contradict each other).")
        return 1

    solution = solver.solve()
    print()
    print("=== SOLUTION FOUND ===")
    print(solution)
    print()
    if count == 1:
        print("[+] Solution analysis: UNIQUE SOLUTION (exactly 1 solution exists).")
    else:
        print("[+] Solution analysis: MULTIPLE SOLUTIONS (at least 2 solutions exist; one is shown above).")
    return 0




def cmd_verify(args) -> int:
    """
    Verify a player's submission against a puzzle. 
    Return the exit code
    """
    print(f"[+] Verifying submission: {args.submission} against puzzle: {args.puzzle}")
    try:
        puzzle = Board.from_file(args.puzzle)
        submission = Board.from_file(args.submission)
    except FileNotFoundError as e:
        print(f"[!] File not found: {e.filename}")
        return 2
    except InvalidBoardFormatError as e:
        print(f"[!] {e}")
        return 1

    report = Verifier(puzzle, submission).verify()

    print()
    print("=== VERIFICATION RESULT ===")
    print(f"Status: {report.status}")
    if report.problems:
        print(f"Problems found ({len(report.problems)}):")
        for problem in report.problems:
            print(f"  - {problem}")

    return 0 if report.status == "VALID SOLUTION" else 1


def main(argv: list[str] | None = None) -> int:
    """Parse the command line and run the chosen command. Return the exit code."""
    args = build_parser().parse_args(argv)
    if args.command == "solve":
        return cmd_solve(args)
    if args.command == "verify":
        return cmd_verify(args)
    return 2 