import argparse

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

def main(argv: list[str] | None = None) -> int:
    """Parse the command line and run the chosen command. Return the exit code."""
    args = build_parser().parse_args(argv)
    print(args)
    return 0