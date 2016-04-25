import tkinter
import random

class ChessBoard:
    def __init__(self):
        self.queens = []
        colors = ("black", "white")
        self.left_border = Border()
        self.right_border = Border()
        self.top_border = Border()
        self.bottom_border = Border()
        self.board = [[self.top_border for i in range(12)]]
        for i in range(1, 9):
            i_color = i % 2
            row = [self.left_border]
            for j in range(1, 9):
                square = SquareContext((i, j), colors[i_color])
                row.append(square)
                i_color = (i_color + 1) % 2
            row.append(self.right_border)
            self.board.append(row)
        self.board.append([self.bottom_border for i in range(12)])

        for i in range(1, 9):
            for j in range(1, 9):
                square = self.board[i][j]
                square.set_right(self.board[i+1][j])
                square.set_down(self.board[i][j+1])
                square.set_downright(self.board[i+1][j+1])
                square.set_downleft(self.board[i-1][j+1])

    def safe_squares(self, row):
        return self.board[row][1].safe_squares_right()

    def draw(self, canvas):
        for row in self.board:
            for square in row:
                square.draw(canvas)


class Border:
    #def threaten_upleft_diagonal(self): pass
    def threaten_downleft(self): pass
    #def threaten_upright(self): pass
    def threaten_downright(self): pass
    #def threaten_left(self): pass
    def threaten_right(self): pass
    #def threaten_up(self): pass
    def threaten_down(self): pass
    #def make_safe_upleft_diagonal(self): pass
    def make_safe_downleft(self): pass
    #def make_safe_upright(self): pass
    def make_safe_downright(self): pass
    #def make_safe_left(self): pass
    def make_safe_right(self): pass
    #def make_safe_up(self): pass
    def make_safe_down(self): pass

    def safe_squares_right(self):
        return []

    def draw(self, canvas): pass


class SquareContext:
    def __init__(self, position, color):
        self.state = SafeSquare(position, color)

    def set_state(self, state):
        self.state = state

    def draw(self, canvas):
        self.state.draw(self, canvas)

    def place_piece(self, piece):
        self.state.place_piece(self, piece)

    def take_piece(self):
        return self.state.take_piece(self)

    def safe_squares_right(self):
        return self.state.safe_squares_right(self)

    def threaten_downleft(self):
        self.state.threaten_downleft(self)

    def threaten_downright(self):
        self.state.threaten_downright(self)

    def threaten_down(self):
        self.state.threaten_down(self)

    def make_safe_downright(self):
        self.state.make_safe_downright(self)

    def make_safe_downleft(self):
        self.state.make_safe_downleft(self)

    def make_safe_down(self):
        self.state.make_safe_down(self)

    def set_right(self, context):
        self.state.set_right(context)

    def set_down(self, context):
        self.state.set_down(context)

    def set_downright(self, context):
        self.state.set_downright(context)

    def set_downleft(self, context):
        self.state.set_downleft(context)

class Square:
    def set_right(self, square):
        self.right = square

    def set_down(self, square):
        self.down = square

    def set_downright(self, square):
        self.downright = square

    def set_downleft(self, square):
        self.downleft = square

    def threaten_downright(self, context):
        self.downright.threaten_downright()

    def threaten_downleft(self, context):
        self.downleft.threaten_downleft()

    def threaten_down(self, context):
        self.right.threaten_down()

    def make_safe_downright(self, context):
        self.upright.make_safe_downright()

    def make_safe_downleft(self, context):
        self.upright.make_safe_downleft()

    def make_safe_down(self, context):
        self.upright.make_safe_down()

class SafeSquare(Square):
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.piece = Piece()

    def place_piece(self, context, piece):
        self.piece = piece
        self.downright.threaten_downright()
        self.downleft.threaten_downleft()
        self.down.threaten_down()

    def take_piece(self, context):
        piece = self.piece
        self.piece = Piece()
        return piece

    def draw(self, context, canvas):
        x, y = self.position
        x2 = x * 100
        y2 = y * 100
        x1 = x2 - 100
        y1 = y2 - 100
        canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
        self.piece.draw(canvas, (x1, y1, x2, y2))

    def safe_squares_right(self, context):
        return [context] + self.right.safe_squares_right()


class ThreatenedSquare(Square):
    def __init__(self, position):
        self.position = position
        self.color = "gray"
        self.piece = Piece()

    def draw(self, canvas):
        x, y = self.position
        x2 = x * 100
        y2 = y * 100
        x1 = x2 - 100
        y1 = y2 - 100
        canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
        self.piece.draw(canvas, (x1, y1, x2, y2))

    def safe_squares_right(self):
        return self.right.safe_squares_right()

class Piece:
    def draw(self, canvas, square): pass


class Queen:
    def draw(self, canvas, square):
        x1, y1, x2, y2 = square
        canvas.create_oval(x1 + 25, y1 + 25, x2 - 25, y2 - 25, fill="red")


if __name__ == '__main__':
    master = tkinter.Tk()
    canvas = tkinter.Canvas(master,
                            width=800,
                            height=800)
    board = ChessBoard()
    safe_squares = board.safe_squares(1)
    if safe_squares:
        random.seed()
        square = random.choice(safe_squares)
        square.place_piece(Queen())
    board.draw(canvas)
    canvas.pack()
    tkinter.mainloop()
