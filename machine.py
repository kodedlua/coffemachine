import curses
from curses import panel
from loader import Loader
import utils
from utils import convertCost

class Machine(object):
    def __init__(self, items, stdscr, loader):
        self.items = items
        self.stdscr = stdscr
        self.template, self.config = loader.load()

    def render(self, height, width, current_rows, selected, balance):
        inputdata = self.config['inputdata']
        balance_cords = inputdata['balance']
        cost_cords = inputdata['cost']
        change_cords = inputdata['change']
        coffe_1_cords = inputdata['coffe-1']
        coffe_1_cost = convertCost(self.items[0][2])
        coffe_2_cords = inputdata['coffe-2']
        coffe_2_cost = convertCost(self.items[1][2])
        coffe_3_cords = inputdata['coffe-3']
        coffe_3_cost = convertCost(self.items[2][2])
        dispenser_1_cords = inputdata['dispenser-1']
        dispenser_1_count = selected.count(self.items[0][0])
        dispenser_2_cords = inputdata['dispenser-2']
        dispenser_2_count = selected.count(self.items[1][0])
        dispenser_3_cords = inputdata['dispenser-3']
        dispenser_3_count = selected.count(self.items[2][0])

        cost = 0 + (self.items[0][2] * dispenser_1_count) + (self.items[1][2] * dispenser_2_count) + (self.items[2][2] * dispenser_3_count)
        cost_text = "00.00"
        if cost != 0:
            cost_text = convertCost(cost)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        win = curses.newwin(height, width, 0, 0)
        for y in range(0, height):
            for x in range(0, width):
                try:
                    if (current_rows == 0) and y == coffe_1_cords['y'] and (x >= 5 and x <=21):
                        win.attron(curses.color_pair(1))
                    elif (current_rows == 1) and y == coffe_2_cords['y'] and (x >= 5 and x <=21):
                        win.attron(curses.color_pair(1))
                    elif (current_rows == 2) and y == coffe_3_cords['y'] and (x >= 5 and x <=21):
                        win.attron(curses.color_pair(1))
                    else:
                        win.attroff(curses.color_pair(1))
                        
                    if (x == balance_cords['x'] and y == balance_cords['y']) or (x == balance_cords['x']+1 and y == balance_cords['y']) or (x == balance_cords['x']+2 and y == balance_cords['y']) or (x == balance_cords['x']+3 and y == balance_cords['y']) or (x == balance_cords['x']+4 and y == balance_cords['y']):
                        offset = x-balance_cords['x']
                        win.addstr(convertCost(balance)[offset])
                    elif (x == cost_cords['x'] and y == cost_cords['y']) or (x == cost_cords['x']+1 and y == cost_cords['y']) or (x == cost_cords['x']+2 and y == cost_cords['y']) or (x == cost_cords['x']+3 and y == cost_cords['y']) or (x == cost_cords['x']+4 and y == cost_cords['y']) or (x == cost_cords['x']+5 and y == cost_cords['y']):
                        offset = x-cost_cords['x']
                        if offset == 0:
                            win.addstr("-")
                        # elif offset == 3:
                        #     win.addstr(".")
                        # else:
                        #     win.addstr("0")
                        else:
                            win.addstr(cost_text[offset-1])
                    elif (x == change_cords['x'] and y == change_cords['y']) or (x == change_cords['x']+1 and y == change_cords['y']) or (x == change_cords['x']+2 and y == change_cords['y']) or (x == change_cords['x']+3 and y == change_cords['y']) or (x == change_cords['x']+4 and y == change_cords['y']):
                        offset = x-cost_cords['x']
                        if offset == 3:
                            win.addstr(".")
                        else:
                            win.addstr("0")
                    elif (x == coffe_1_cords['x'] and y == coffe_1_cords['y']) or (x == coffe_1_cords['x']+1 and y == coffe_1_cords['y']) or (x == coffe_1_cords['x']+2 and y == coffe_1_cords['y']) or (x == coffe_1_cords['x']+3 and y == coffe_1_cords['y']) or (x == coffe_1_cords['x']+4 and y == coffe_1_cords['y']):
                        offset = x-coffe_1_cords['x']
                        win.addstr(coffe_1_cost[offset])
                    elif (x == coffe_2_cords['x'] and y == coffe_2_cords['y']) or (x == coffe_2_cords['x']+1 and y == coffe_2_cords['y']) or (x == coffe_2_cords['x']+2 and y == coffe_2_cords['y']) or (x == coffe_2_cords['x']+3 and y == coffe_2_cords['y']) or (x == coffe_2_cords['x']+4 and y == coffe_2_cords['y']):
                        offset = x-coffe_2_cords['x']
                        win.addstr(coffe_2_cost[offset])
                    elif (x == coffe_3_cords['x'] and y == coffe_3_cords['y']) or (x == coffe_3_cords['x']+1 and y == coffe_3_cords['y']) or (x == coffe_3_cords['x']+2 and y == coffe_3_cords['y']) or (x == coffe_3_cords['x']+3 and y == coffe_3_cords['y']) or (x == coffe_3_cords['x']+4 and y == coffe_3_cords['y']):
                        offset = x-coffe_3_cords['x']
                        win.addstr(coffe_3_cost[offset])
                    else:
                        win.addstr(y, x, self.template[y][x])
                except curses.error as e:
                    pass
        if dispenser_1_count > 0:
            win.addstr(dispenser_1_cords['y'], dispenser_1_cords['x'], f"x{dispenser_1_count} black")
        if dispenser_2_count > 0:
            win.addstr(dispenser_2_cords['y'], dispenser_2_cords['x'], f"x{dispenser_2_count} cappucino")
        if dispenser_3_count > 0:
            win.addstr(dispenser_3_cords['y'], dispenser_3_cords['x'], f"x{dispenser_3_count} latte")
        return win

    def renderHelpBox(self, height, maxwidth):
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        helpBox = curses.newwin(5, maxwidth, height+4, 0)
        helpBox.attron(curses.color_pair(2))
        helpBox.addstr("[UP KEY] [DOWN KEY] - navigate | [E] - select | [R] - remove | [Q] - exit")
        return helpBox

    def display(self):
        curses.initscr()
        # get max size of terminal
        rows, cols = self.stdscr.getmaxyx()
        height = len(self.template)
        width = len(self.template[0])
        # if terminal size isn't big enough exit
        if rows < height or cols < width:
            print("This app is not supported in this terminal! (width and height is not big enough)")
            exit(1)

        current_row = 0
        selected = []

        while True:
            win = self.render(height, width, current_row, selected, 00.00)
            win.refresh()
            helpBox = self.renderHelpBox(height, cols)
            helpBox.refresh()
            self.stdscr.refresh()
            event = self.stdscr.getch()
            if event == curses.KEY_UP:
                if current_row-1 >= 0:
                    current_row-=1
            elif event == curses.KEY_DOWN:
                if current_row+1 <= 3:
                    current_row+=1
            elif event == ord("e"):
                if current_row <= 2:
                    if selected.count(self.items[current_row][0])+1 <= 9:
                        selected.append(self.items[current_row][0])
            elif event == ord("r"):
                if current_row <= 2:
                    if selected.count(self.items[current_row][0])-1 >= 0:
                        selected.pop(selected.index(self.items[current_row][0]))
            elif event == ord("q"):
                break