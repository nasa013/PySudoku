


class SudokuError(Exception):
    """Base class for all PySudoku errors."""
    def __init__(self, *args):
        super().__init__(*args)


class InvalidBoardFormatError(SudokuError):
    """Raised when the file content is malformed (wrong shape or bad characters)."""
    def __init__(self, *args):
        super().__init__(*args)


class InvalidBoardError(SudokuError):
    """Raised when the starting board repeats a digit in a row, column or box."""
    def __init__(self, conflicts: list[str]) -> None:
        super().__init__("The board has conflicts")
        self.conflicts = conflicts

