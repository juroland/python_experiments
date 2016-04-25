import tkinter
import random

class ChessBoard:
    def __init__(self):
        self.queens = []
        colors = ("black", "white")
        self.rows = []
        self.left_border = Border()
        self.right_border = Border()
        self.top_border = Border()
        self.bottom_border = Border()
        for i in range(1, 9):
            i_color = i % 2
            row = []
            for j in range(1, 9):
                square = SquareContext((i, j), colors[i_color])
                row.append(square)
                i_color = (i_color + 1) % 2
            self.rows.append(row)

        for i in range(len(self.rows)-1):
            for j, square in enumerate(self.rows[i]):
                square.set_down(self.rows[i+1][j])

        for square in self.rows[-1]:
            square.set_down(self.bottom_border)


    def safe_squares(self, row):
        return self.rows[row][0].safe_squares_down()

    def draw(self, canvas):
        for row in self.rows:
            for square in row:
                square.draw(canvas)


class Border:
    #def threaten_upleft_diagonal(self): pass
    #def threaten_downleft_diagonal(self): pass
    def threaten_upright_diagonal(self): pass
    def threaten_downright_diagonal(self): pass
    #def threaten_left(self): pass
    def threaten_right(self): pass
    #def threaten_up(self): pass
    #def threaten_down(self): pass
    #def make_safe_upleft_diagonal(self): pass
    #def make_safe_downleft_diagonal(self): pass
    def make_safe_upright_diagonal(self): pass
    def make_safe_downright_diagonal(self): pass
    #def make_safe_left(self): pass
    def make_safe_right(self): pass
    #def make_safe_up(self): pass
    #def make_safe_down(self): pass

    def safe_squares_down(self):
        return []


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

    def safe_squares_down(self):
        return self.state.safe_squares_down(self)

    def threaten_upright_diagonal(self):
        self.upright.threaten_upright()

    def threaten_downright_diagonal(self):
        self.downright.threaten_downright()

    def threaten_right(self):
        self.right.threaten_right()

    def make_safe_upright_diagonal(self):
        self.upright.make_safe_upright()

    def make_safe_downright_diagonal(self):
        self.upright.make_safe_downright()

    def make_safe_right(self):
        self.upright.make_safe_right()

    def set_right(self, context):
        self.state.set_right(context)

    def set_down(self, context):
        self.state.set_down(context)

    def set_upright(self, context):
        self.state.set_upright(context)

    def set_downright(self, context):
        self.state.set_downright(context)


class SafeSquare:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.piece = Piece()

    def place_piece(self, context, piece):
        self.piece = piece

    def take_piece(self, context):
        piece = self.piece
        self.piece = Piece()
        return piece

    def draw(self, context, canvas):
        x, y = self.position
        print(x, y)
        x2 = x * 100
        y2 = y * 100
        x1 = x2 - 100
        y1 = y2 - 100
        canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
        self.piece.draw(canvas, (x1, y1, x2, y2))

    def safe_squares_down(self, context):
        return [context] + self.down.safe_squares_down()

    def set_right(self, context):
        self.right = context

    def set_down(self, context):
        self.down = context

    def set_upright(self, context):
        self.upright = context

    def set_downright(self, context):
        self.downright = context

class ThreatenedSquare:
    def __init__(self, position):
        self.position = position
        self.color = "gray"
        self.piece = Piece()

    def draw(self, canvas):
        x, y = self.position
        print(x, y)
        x2 = x * 100
        y2 = y * 100
        x1 = x2 - 100
        y1 = y2 - 100
        canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
        self.piece.draw(canvas, (x1, y1, x2, y2))

    def safe_squares_down(self):
        return self.down.safe_squares_down()

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
    safe_squares = board.safe_squares(0)
    random.seed()
    square = random.choice(safe_squares)
    square.place_piece(Queen())
    board.draw(canvas)
    canvas.pack()
    tkinter.mainloop()
