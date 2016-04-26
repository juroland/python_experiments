import tkinter
import random
import math

class ChessBoard:
    def __init__(self, width):
        self.queens = []
        colors = ("black", "white")
        threatened_colors = ("red4", "red2")
        self.border = Border()

        self.board = [[self.border] * 12]
        for i in range(1, 9):
            i_color = i % 2
            row = [self.border]
            for j in range(1, 9):
                square = Square((j, i), colors[i_color],
                                threatened_colors[i_color], width/8)
                row.append(square)
                i_color = (i_color + 1) % 2
            row.append(self.border)
            self.board.append(row)
        self.board.append([self.border] * 12)

        for i in range(1, 9):
            for j in range(1, 9):
                square = self.board[i][j]
                square.set_neighbor("right", self.board[i][j+1])
                square.set_neighbor("left", self.board[i][j-1])
                square.set_neighbor("down", self.board[i+1][j])
                square.set_neighbor("up", self.board[i-1][j])
                square.set_neighbor("downright", self.board[i+1][j+1])
                square.set_neighbor("upright", self.board[i-1][j-1])
                square.set_neighbor("downleft", self.board[i+1][j-1])
                square.set_neighbor("upleft", self.board[i+1][j+1])

    def safe_squares(self, row):
        return self.board[row][1].safe_squares_right()

    def draw(self, canvas):
        for row in self.board:
            for square in row:
                square.draw(canvas)


class Border:
    def threaten(self, direction): pass

    def make_safe(self, direction): pass

    def safe_squares_right(self):
        return []

    def draw(self, canvas): pass


class Square:
    directions = ["left", "right", "up", "down", "upleft", "upright",
                  "downleft", "downright"]
    def __init__(self, position, color, threatened_color, width):
        self.state = SafeSquare()
        self.position = position
        self.color = color
        self.threatened_color = threatened_color
        self.piece = Piece()
        self.width = width

    def set_state(self, state):
        self.state = state

    def draw(self, canvas):
        self.state.draw(self, canvas, self.width)

    def safe_squares_right(self):
        return self.state.safe_squares_right(self)

    def threaten(self, direction):
        self.state.threaten(self)
        getattr(self, direction).threaten(direction)

    def make_safe(self, direction):
        self.state.make_safe(self)
        getattr(self, direction).make_safe(direction)

    def set_neighbor(self, direction, square):
        setattr(self, direction, square)

    def place_piece(self, piece):
        self.piece = piece
        for direction in Square.directions:
            getattr(self, direction).threaten(direction)

    def take_piece(self):
        piece = self.piece
        self.piece = Piece()
        for direction in Square.directions:
            getattr(self, direction).make_safe(direction)
        return piece


class SafeSquare:
    def draw(self, context, canvas, width):
        x, y = context.position
        x2 = x * width
        y2 = y * width
        x1 = x2 - width
        y1 = y2 - width
        canvas.create_rectangle(x1, y1, x2, y2, fill=context.color)
        context.piece.draw(canvas, (x1, y1, x2, y2))

    def safe_squares_right(self, context):
        return [context] + context.right.safe_squares_right()

    def threaten(self, context):
        context.set_state(ThreatenedSquare())

    def make_safe(self, context): pass


class ThreatenedSquare:
    def __init__(self):
        self.n_threat = 1

    def draw(self, context, canvas, width):
        x, y = context.position
        x2 = x * width
        y2 = y * width
        x1 = x2 - width
        y1 = y2 - width
        canvas.create_rectangle(x1, y1, x2, y2, fill=context.threatened_color)
        context.piece.draw(canvas, (x1, y1, x2, y2))

    def safe_squares_right(self, context):
        return context.right.safe_squares_right()

    def threaten(self, context):
        self.n_threat = self.n_threat + 1

    def make_safe(self, context):
        self.n_threat = self.n_threat - 1
        if self.n_threat == 0:
            context.set_state(SafeSquare())


class Piece:
    def draw(self, canvas, square): pass


class Queen:
    def draw(self, canvas, square):
        x1, y1, x2, y2 = square
        delta = math.fabs(x1 - x2)/4
        canvas.create_oval(x1 + delta, y1 + delta, x2 - delta, y2 - delta, fill="red")


class Backtrack:
    def __init__(self, canvas, board):
        self.canvas = canvas
        self.board = board
        self.queen_index = 1
        self.safe_squares = self.board.safe_squares(self.queen_index)
        self.board.draw(canvas)
        self.stack = []

    def step(self):
        if self.queen_index == 9:
            return
        if self.safe_squares:
            square = self.safe_squares.pop()
            self.stack.append((square, self.safe_squares))
            square.place_piece(Queen())
            self.queen_index = self.queen_index + 1
            self.safe_squares = self.board.safe_squares(self.queen_index)
        elif self.stack:
            square, self.safe_squares = self.stack.pop()
            square.take_piece()
            self.queen_index = self.queen_index - 1
        self.board.draw(canvas)


if __name__ == '__main__':
    master = tkinter.Tk()
    size = 800
    canvas = tkinter.Canvas(master,
                            width=size,
                            height=size)
    board = ChessBoard(width=size)
    backtrack = Backtrack(canvas, board)
    canvas.pack()

    step_time = 500
    def task():
        backtrack.step()
        master.after(step_time, task)

    master.after(step_time, task)
    tkinter.mainloop()
