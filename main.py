import curses
from curses import wrapper, panel
from machine import Machine
from loader import Loader

latte_price = 0.00
black_price = 0.00
cappucino_price = 0.00

class App(object):
    def __init__(self, stdscr):
        self.screen = stdscr
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        loader = Loader()

        items = [("coffe-1", "black coffee", 1.55), ("coffe-2", "cappucino", 0.90), ("coffe-3", "latte", 2.20)]
        machine = Machine(items, self.screen, loader)
        machine.display()


if __name__ == '__main__':
    wrapper(App)