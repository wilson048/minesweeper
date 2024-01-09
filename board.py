import random

class Cell:
    def __init__(self):
        """ A cell class for representing cells on the Minesweeper board """
        self.num_bombs = 0
        self.revealed = False
        self.flagged = False

    def get_num_mines(self):
        """ Returns the number of bo  mbs around the cell """
        return self.num_bombs

    def is_flagged(self):
        """ Returns true if the cell is flagged on the board"""
        return self.flagged

    def is_revealed(self):
        """ Returns true if the cell is revealed on the board"""
        return self.revealed

    def set_num_mines(self, bombs):
        """ Sets the number of bombs around the cell (done in Grid class) """
        self.num_bombs = bombs

    def reveal(self):
        """ Reveals the cell and un-flags it"""
        self.revealed = True
        self.flagged = False

    def flag(self):
        """ Flags the cell only if it isn't revealed"""
        if self.revealed:
            return
        self.flagged = not self.flagged

    def __str__(self):
        """ Returns a string representation of what a cell has which is its reveal status, its flagged status,
        and the number of mines around it """
        return "Cell Revealed: " + str(self.revealed) + \
               " Flagged: " + str(self.flagged) + " " \
                                                  "Num: " + str(self.num_bombs)


# Mine class for representing mines on the grid
class Mine(Cell):
    def __init__(self):
        """ A Mine class for representing mines on the Minesweeper board (inherits from Cell)"""
        super(Mine, self).__init__()

    def __str__(self):
        """ Returns a string representation of what a mine has which is its reveal status and its flagged status"""
        return "Mine Revealed: " + str(self.revealed) + " Flagged: " + str(self.flagged)


class Grid:
    def __init__(self, rows, columns):
        """ A grid class that contains a board for holding and modifying cells on the grid """
        self.rows = rows
        self.columns = columns
        self.board = []
        self.create_board()

    def create_board(self):
        """ Constructs the board inside the grid class and assigns numbers to each non-Mine cell """
        # Populate the board
        for x in range(self.rows):
            row = []
            for y in range(self.columns):
                num = random.randint(1, 100)
                # mess with odds of mines here
                if num <= 20:
                    cell = Mine()
                else:
                    cell = Cell()
                row.append(cell)
            self.board.append(row)
        # set numbers to the board
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                temp = 0
                if isinstance(self.board[x][y], Mine):
                    # Mines are given an impossible number
                    self.board[x][y].set_num_mines(9)
                else:
                    # count the number of mines around a cell
                    for i in range(3):
                        i += x - 1
                        for j in range(3):
                            j += y - 1
                            if self.in_bounds(i, j) and isinstance(self.board[i][j], Mine):
                                temp += 1
                    self.board[x][y].set_num_mines(temp)

    def reveal_board(self, x, y):
        """ Method that recursively reveals the board starting at the given point if the amount of bombs is 0
        This method does nothing if the game is over"""
        # Base case 1: The game is over
        if self.has_won() or self.has_lost():
            return
        # Base case 2: The point is out of bounds or is a revealed cell
        if not self.in_bounds(x, y) or self.board[x][y].is_revealed():
            return
        self.board[x][y].reveal()
        # Base case 3: The point contains at least 1 mine around it
        if self.board[x][y].get_num_mines() != 0:
            return
        # Recursive Case: reveal every cell around the cell with 0 mines around it
        for i in range(3):
            i += x - 1
            for j in range(3):
                j += y - 1
                self.reveal_board(i, j)

    def reveal_unflagged(self, x, y):
        """ Method for revealing any un-flagged cells around a revealed cell
        Un-flagged cells are only revealed if the number of flags around
        the cell equal the number of mines around it
        This method does nothing if the game is over"""
        if self.has_won() or self.has_lost():
            return
        flags = 0
        for i in range(3):
            i += x - 1
            for j in range(3):
                j += y - 1
                if self.in_bounds(i, j) and self.get_cell(i, j).is_flagged():
                    flags += 1
        if flags == self.board[x][y].get_num_mines():
            for i in range(3):
                i += x - 1
                for j in range(3):
                    j += y - 1
                    if self.in_bounds(i, j) and not self.get_cell(i, j).is_flagged():
                        self.reveal_board(i, j)

    def in_bounds(self, x, y):
        """ Returns true if the given point is in the bounds of the board """
        return 0 <= x < len(self.board) and 0 <= y < len(self.board[0])

    def get_board(self):
        """ Returns the board stored in Grid """
        return self.board

    def has_lost(self):
        """ Returns true if the game has been lost. A loss happens when a mine is revealed on the board """
        for x in range(self.rows):
            for y in range(self.columns):
                if self.get_cell(x, y).is_revealed() and isinstance(self.get_cell(x, y), Mine):
                    return True
        return False

    def has_won(self):
        """ Returns true if the game has been won. A win happens when all non-mine cells are revealed and when
        all mine cells are flagged"""
        for x in range(self.rows):
            for y in range(self.columns):
                if isinstance(self.get_cell(x, y), Mine) and not self.get_cell(x, y).is_flagged():
                    return False
                if not isinstance(self.get_cell(x, y), Mine) and not self.get_cell(x, y).is_revealed():
                    return False
        return True

    def reveal_mines(self):
        """ Method for revealing mines. This is meant to happen when the game is over"""
        for i in range(self.rows):
            for j in range(self.columns):
                if not self.board[i][j].is_flagged() and isinstance(self.get_cell(i, j), Mine):
                    self.board[i][j].reveal()

    def flag_board(self, x, y):
        """ Flags the board at the specified coordinate, making sure it is in-bounds in the process
        This method does nothing if the game is over"""
        if self.has_won() or self.has_lost():
            return
        if self.in_bounds(x, y):
            self.board[x][y].flag()

    def get_cell(self, x, y):
        """ Returns the cell at the given coordinate """
        return self.board[x][y]

    def get_rows(self):
        """ Returns the number of rows on the grid """
        return self.rows

    def get_cols(self):
        """ Returns the number of columns on the grid"""
        return self.columns

    def __str__(self):
        """ Returns a string representation of the board. Cells are marked with the number of mines around them while
        Mines are marked with an asterisk "*" """
        board_str = ""
        for x in range(len(grid.get_board())):
            board_str += "[ "
            for y in range(len(grid.get_board()[x])):
                if isinstance(self.board[x][y], Mine):
                    board_str += "*, "
                else:
                    board_str += str(self.board[x][y].get_num_mines()) + ", "
            board_str += "]\n"
        return board_str