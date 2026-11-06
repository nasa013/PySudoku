import unittest
from pysudoku.board import Board
from pysudoku.exceptions import InvalidBoardFormatError


class TestBoard(unittest.TestCase):
    def test_eight_rows_raises(self):
        text = "\n".join(["530070000"] * 8)
        with self.assertRaises(InvalidBoardFormatError):
            Board.from_string(text)

    