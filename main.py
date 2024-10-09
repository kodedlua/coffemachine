import curses
from curses import wrapper, panel
from machine import Machine
from loader import Loader

class App(object):
    def __init__(self, stdscr, balance):
        self.screen = stdscr
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        loader = Loader()

        items = [("coffe-1", "black coffee", 1.55), ("coffe-2", "cappucino", 0.90), ("coffe-3", "latte", 2.20)]
        machine = Machine(items, balance, self.screen, loader)
        machine.display()


if __name__ == '__main__':
    balance = float(input("Set balance (dd.ff): "))
    wrapper(App, balance)