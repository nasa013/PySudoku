from pathlib import Path

from .exceptions import InvalidBoardFormatError



# helper method
def _parse_row(line: str, row_number: int) -> list[int] | None:
    """
    Turn one text line into a list of ints, or None if the line is only a divider
    """

    # remove the seperators 
    for ch in "|-+":
        line = line.replace(ch, "")
    line = line.strip()

    if not line:
        return None  # it was a divider 
    
    pieces = line.split()

    if len(pieces) == 1:          
        pieces = list(pieces[0])  

    row = []

    for piece in pieces:
        if piece == ".":
            row.append(0)
        elif len(piece) == 1 and piece in "0123456789":
            row.append(int(piece))
        else:
            raise InvalidBoardFormatError(
                f"Row {row_number} has an invalid cell: '{piece}'"
            )
    return row






class board:
    def __init__(self, grid: list[list[int]]):
        '''
        set up the objects memory
        it stores two things on the object: the grid, and the set of given cells
        '''
        self._grid=  [ row[:] for row in grid ]  # copy each row
        self._givens= {
        (r, c) for r in range(SIZE) for c in range(SIZE) if grid[r][c] != 0
        } #collect (r, c) for every row r and column c, only if the cell is not 0



    @classmethod
    def from_string(cls, text: str): 
        """
        
        """
        rows= []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            row = _parse_row(line, len(rows) + 1)
            if row == None:
                continue

            if len(row) != 9 :
                raise InvalidBoardFormatError(f"Row {len(row)+1} has {len(row)} cells, expected 9")
            rows.append(row)

        if len(rows) != 9 :
            raise InvalidBoardFormatError
        return cls(rows) 


    @classmethod
    def from_file(cls, path):
        text = Path(path).read_text(encoding="utf-8")
        return cls.from_string(text)

    

    def get(self, r: int, c: int) -> int:
        ...


    def set(self, r: int, c: int, value: int) -> None:
        ...  

    def is_given(self, r: int, c: int) -> bool: 
        ...


    def empty_cells(self) -> list[tuple[int, int]]:
        ...


    def find_conflicts(self) -> list[str]:
        ...


    def copy(self):
        
        ...


    def __str__(self) -> str:
        ...

    