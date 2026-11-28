import unittest
from pathlib import Path

from pysudoku.board import Board
from pysudoku.verifier import Verifier

DATA = Path(__file__).parent / "data"


def verify(submission_file: str):
    puzzle = Board.from_file(DATA / "puzzle.txt")
    submission = Board.from_file(DATA / submission_file)
    return Verifier(puzzle, submission).verify()


class TestVerifier(unittest.TestCase):
    def test_sample_submission(self):
        """
        the sample submission has the 4 problems from the spec, in order.
        """
        report = verify("player_submission.txt")
        self.assertEqual(report.status, "INVALID SOLUTION")
        self.assertEqual(report.problems, [
            "Row 9, Column 1: cell is empty.",
            "Row 2: number 8 appears in columns 3 and 9.",
            "Column 3: number 8 appears in rows 2 and 3.",
            "Box 1: number 8 appears at (2, 3) and (3, 3).",
        ])

    def test_correct_solution(self):
        """
        the correct solution is VALID with no problems
        """
        report = verify("solution.txt")
        self.assertEqual(report.status, "VALID SOLUTION")
        self.assertEqual(report.problems, [])

    def test_one_empty_cell(self):
        """
        one non-given cell set to 0 is INCOMPLETE
        """
        report = verify("solution_one_empty.txt")
        self.assertEqual(report.status, "INCOMPLETE")
        self.assertEqual(report.problems, ["Row 9, Column 1: cell is empty."])

    def test_changed_given(self):
        """
        changing a given is INVALID, and that problem comes first.
        """
        report = verify("solution_changed_given.txt")
        self.assertEqual(report.status, "INVALID SOLUTION")
        self.assertEqual(
            report.problems[0],
            "Row 1, Column 1: value 3 overwrites the given number 5.",
        )


if __name__ == "__main__":
    unittest.main()
