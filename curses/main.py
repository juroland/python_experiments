import curses
import locale
import random

locale.setlocale(locale.LC_ALL, '')    # set your locale

# https://en.wikipedia.org/wiki/Box_Drawing

class Maze:
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.x_begin = 1
        self.y_begin = 1
        self.x_end = x_size - 2
        self.y_end = y_size - 2;
        self.maze = [[0 for y in range(y_size)] for x in range(x_size)]
        self.maze[1][0] = 1
        self.maze[-2][-1] = 1

    def get_neighbors(self, x, y, direction):
        assert (direction[0] == 0 or direction[1] == 0,
                "directions are up, down, left, or right")
        neighbors = []
        x += direction[0]
        y += direction[1]
        if direction[0] == 0:
            coordinates = [(x, y), (x-1, y), (x+1, y)]
        else:
            coordinates = [(x, y), (x, y-1), (x, y+1)]

        for x, y in coordinates:
            if (self.x_begin <= x <= self.x_end
                    and self.y_begin <= y <= self.y_end):
                neighbors.append((x,y))

        return neighbors

    def are_neighbors_free(self, neighbors):
        return all(self.maze[x][y] == 0 for x, y in neighbors)

    def get_free_neighbors(self, x, y):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x0, y0 in directions:
            directed_neighbors = self.get_neighbors(x, y, (x0, y0))
            directed_neighbors.extend(self.get_neighbors(x, y, (2*x0, 2*y0)))
            if (directed_neighbors != []
                    and self.are_neighbors_free(directed_neighbors)):
                neighbors.append((x+x0, y+y0))
        return neighbors

    def count(self, nodes):
        count = 0;
        for v in nodes:
            count += self.maze[v[0]][v[1]]
        return count


def depth_first_generator(x_size, y_size):
    stack = [(x_size-2,y_size-2)]
    M = Maze(x_size, y_size)
    M.maze[x_size-2][y_size-2] = 1
    while len(stack) > 0:
        x, y = stack[-1]
        neighbors = M.get_free_neighbors(x, y)
        if neighbors == []:
            stack.pop()
        else:
            random.shuffle(neighbors)
            x, y = neighbors[0]
            M.maze[x][y] = 1
            stack.append((x, y))

    return M.maze

def main(stdscr):
    stdscr.clear()
    curses.curs_set(False) # Invisible cursor
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.addstr(0, 0, '{} x {}'.format(curses.LINES, curses.COLS),
                  curses.color_pair(1))
    maze = depth_first_generator(curses.LINES-2, curses.COLS-2)
    for x in range(1, curses.LINES-1):
        for y in range(1, curses.COLS-1):
            if maze[x-1][y-1] != 1:
                stdscr.addstr(x, y, ' ', curses.color_pair(1) | curses.A_BOLD)

    stdscr.refresh()
    while True:
        c = stdscr.getch()
    stdscr.getkey()

curses.wrapper(main)
#maze = depth_first_generator(10, 12)
#print(maze)
