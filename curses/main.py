import curses

def main(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.addstr(0, 0, '{} x {}'.format(curses.LINES, curses.COLS), curses.color_pair(1))
    stdscr.addstr(1, 0, "X", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)
