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
    def from_string(cls, text: str) -> "Board": 
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

    

    def set(self, r: int, c: int, value: int) -> None :
        if (r ,c) in self._givens:
            raise ValueError("Cannot modify a given cell")
        self._grid[r][c]= value



    def is_given(self, r: int, c: int) -> bool: 


        return (r, c) in self._givens 




    def empty_cells(self) -> list[tuple[int, int]]:
        """
        input: board 
        check for every row by column for 0's valuse 
        store them as a tuple in a list 
        return: 
        list of int tuples
        
        """
        empty=[]
        for r in range(9):
            for c in range(9):
                if self._grid[r][c] == 0 :
                    empty.append((r ,c))

        return empty 




    def find_conflicts(self) -> list[str] :
        """
        sudoku rules 
        - a number must not repeat in the same row of column 
        - a number must not repeat inside the same 3×3 box.

        first we check for rows and stores their occurance in a dictionary 
        the check for columns 
       and the last is for boxes
        """
        conflicts= []
        for r in range(9):
            seen = {} # stores number and their postion
            for c in range(9):
                value= self._grid[r][c]
                if value == 0 :
                    continue
                seen.setdefault(value, []).append(c + 1) #If the number already exists as a key, get its list.If it doesn't exist, create a new empty list.
            for num , col in seen.items():
                if len(col) >= 2 :
                    conflicts.append(f"Row {r + 1}: number {num} appears in columns {col[0]} and {col[1]}.")

        for c in range(9):
            seen={}
            for r in range(9):
                value = self._grid[r][c]

                if value == 0 :
                    continue
                seen.setdefault(value,[]).append(r+1)
            for num , row in seen.items():
                if len(row) >= 2:
                    conflicts.append(f"Column {c + 1}: number {num} appears in rows {row[0]} and {row[1]}.")

        for i in range(9):
            r_start = i // 3 * 3
            c_start=  i % 3 * 3

            seen = {}  
            for r in range(r_start, r_start + 3):
                for c in range(c_start, c_start + 3):
                    value = self._grid[r][c]
                    if value == 0:
                        continue
                    seen.setdefault(value, []).append((r + 1, c + 1))

            for num, places in seen.items():
                if len(places) >= 2:
                    (r1, c1), (r2, c2) = places[0], places[1]
                    conflicts.append(
                        f"Box {i + 1}: number {num} appears at ({r1}, {c1}) and ({r2}, {c2})."
                    )

        return conflicts






    def copy(self) -> "Board":
        
        """Return an independent Board """

        new = Board(self._grid)
        new._givens = set(self._givens)
        return new


    def __str__(self) -> str :
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

    




    