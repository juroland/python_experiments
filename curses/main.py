import curses
import locale
import random

locale.setlocale(locale.LC_ALL, '')    # set your locale

# https://en.wikipedia.org/wiki/Box_Drawing

class Maze:
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.maze = [[0 for y in range(y_size)] for x in range(x_size)]
        self.maze[1][0] = 1
        self.maze[-2][-1] = 1

    def top_neighbors(self, x, y):
        neighbors = []
        if x > 1:
            neighbors.append((x-1, y))
            if y > 1:
                neighbors.append((x-1, y-1))
            if y < self.y_size-2:
                neighbors.append((x-1, y+1))
        return neighbors

    def bottom_neighbors(self, x, y):
        neighbors = []
        if x < self.x_size-2:
            neighbors.append((x+1, y))
            if y > 1:
                neighbors.append((x+1, y-1))
            if y < self.y_size-2:
                neighbors.append((x+1, y+1))
        return neighbors

    def left_neighbors(self, x, y):
        neighbors = []
        if y > 1:
            neighbors.append((x, y-1))
            if x > 1:
                neighbors.append((x-1, y-1))
            if x < self.x_size-2:
                neighbors.append((x+1, y-1))
        return neighbors

    def right_neighbors(self, x, y):
        neighbors = []
        if y < self.y_size-2:
            neighbors.append((x, y+1))
            if x > 1:
                neighbors.append((x-1, y+1))
            if x < self.y_size-2:
                neighbors.append((x+1, y+1))
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
        u = stack[-1]
        x = u[0]
        y = u[1]
        neighbors = []
        if x-1 >= 1 and M.maze[x-1][y] == 0:
            neighbors.append((x-1,y))
        if y-1 >= 1 and M.maze[x][y-1] == 0:
            neighbors.append((x,y-1))
        if x+1 < x_size-1 and M.maze[x+1][y] == 0:
            neighbors.append((x+1,y))
        if y+1 < y_size-1 and M.maze[x][y+1] == 0:
            neighbors.append((x,y+1))

        if len(neighbors) == 0:
            stack.pop()
            continue

        random.shuffle(neighbors)
        for v in neighbors:
            if v[1] < y:
                if M.count(M.left_neighbors(x,y)) == 0:
                    M.maze[v[0]][v[1]] = 1
                    stack.append(v)
                else:
                    M.maze[v[0]][v[1]] = -1
                break
            if v[1] > y:
                if M.count(M.right_neighbors(x,y)) == 0:
                    M.maze[v[0]][v[1]] = 1
                    stack.append(v)
                else:
                    M.maze[v[0]][v[1]] = -1
                break
            if v[0] < x:
                if M.count(M.top_neighbors(x,y)) == 0:
                    M.maze[v[0]][v[1]] = 1
                    stack.append(v)
                else:
                    M.maze[v[0]][v[1]] = -1
                break
            if v[0] > x:
                if M.count(M.bottom_neighbors(x,y)) == 0:
                    M.maze[v[0]][v[1]] = 1
                    stack.append(v)
                else:
                    M.maze[v[0]][v[1]] = -1
                break

    return M.maze

def main(stdscr):
    stdscr.clear()
    curses.curs_set(False) # Invisible cursor
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.addstr(0, 0, '{} x {}'.format(curses.LINES, curses.COLS),
                  curses.color_pair(1)) 
    maze = depth_first_generator(curses.LINES-2, curses.COLS-2)
    for x in range(1, curses.LINES-1):
        for y in range(1, curses.COLS-1):
            if maze[x-1][y-1] != 1:
                stdscr.addstr(x, y, ' ',
                              curses.color_pair(1) | curses.A_BOLD)

    stdscr.refresh()
    while True:
        c = stdscr.getch()
    stdscr.getkey()

curses.wrapper(main)
#maze = depth_first_generator(10, 12)
#print(maze)
