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






class Board:
    def __init__(self, grid: list[list[int]]):
        '''
        set up the objects memory
        it stores two things on the object: the grid, and the set of given cells
        '''
        self._grid=  [ row[:] for row in grid ]  # copy each row
        self._givens= {
        (r, c) for r in range(9) for c in range(9) if grid[r][c] != 0
        } #collect (r, c) for every row r and column c, only if the cell is not 0



    @classmethod
    def from_string(cls, text: str): 
        """
        read a board from a text file
        parse the text -->  check conditions for lines 
        return a board for initialization an object

        """
        rows= []
        for line in text.splitlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            row = _parse_row(line, len(rows) + 1)

            if row is  None:
                continue

            if len(row) != 9 :
                raise InvalidBoardFormatError(f"Row {len(rows)+1} has {len(row)} cells, expected 9")
            rows.append(row)

        if len(rows) != 9 :
            raise InvalidBoardFormatError(f"Found {len(rows)} rows, expected 9")
        return cls(rows) 


    @classmethod
    def from_file(cls, path):
        """
        load a board from a file --- > text 
        return  a class board
        
        """
        text = Path(path).read_text(encoding="utf-8")
        return cls.from_string(text)

    

    def get(self, r: int, c: int) -> int:
        '''
        return the digit at grid(r,c)
        '''
        return self._grid[r][c]

    

    def set(self, r: int, c: int, value: int) -> None:
        self._grid[r][c]= value



    def is_given(self, r: int, c: int) -> bool: 


        return (r, c) in self._givens




    def empty_cells(self) -> list[tuple[int, int]]:
        """Return the (r, c) of every empty cell, row by row."""
        return [
            (r, c) for r in range(9) for c in range(9) if self._grid[r][c] == 0
        ]




    def find_conflicts(self) -> list[str]:
        conflicts= []
        



    def copy(self):
        
        """Return an independent Board that keeps the same givens."""

        new = Board(self._grid)
        new._givens = set(self._givens)
        return new


    def __str__(self):
        """
        to print the board 
        reverse the steps and add the seperators 
        first we loop throuh rows
        then we go inside columns to write the board like 0 becomes . 
        
        
        """



        lines=[]
        divider = "------+-------+------"
        for r in range(9):
            if r == 3 or r == 6 :
                lines.append(divider)
            groups=[]
            for start in (0, 3, 6):

                cells = self._grid[r][start:start + 3]

                groups.append(" ".join("." if n == 0 else str(n) for n in cells)) 

            lines.append(" | ".join(groups))
        return "\n".join(lines)

    




    