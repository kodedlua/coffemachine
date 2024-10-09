import curses
from curses import panel
from loader import Loader
import utils
from utils import formatNumber

class Machine(object):
    def __init__(self, items, balance, stdscr, loader):
        self.items = items
        self.balance = balance
        self.stdscr = stdscr
        self.template, self.config = loader.load()

    def renderMachine(self, height, width, selectedRows, selected, balance):
        # load all data and format it
        inputdata = self.config['inputdata']
        balance_cords = inputdata['balance']
        cost_cords = inputdata['cost']
        change_cords = inputdata['change']
        coffe_1_cords = inputdata['coffe-1']
        coffe_1_cost = formatNumber(self.items[0][2])
        coffe_2_cords = inputdata['coffe-2']
        coffe_2_cost = formatNumber(self.items[1][2])
        coffe_3_cords = inputdata['coffe-3']
        coffe_3_cost = formatNumber(self.items[2][2])
        dispenser_1_cords = inputdata['dispenser-1']
        dispenser_1_count = selected.count(self.items[0][0])
        dispenser_2_cords = inputdata['dispenser-2']
        dispenser_2_count = selected.count(self.items[1][0])
        dispenser_3_cords = inputdata['dispenser-3']
        dispenser_3_count = selected.count(self.items[2][0])

        # format cost
        cost = 0 + (self.items[0][2] * dispenser_1_count) + (self.items[1][2] * dispenser_2_count) + (self.items[2][2] * dispenser_3_count)
        cost_text = "00.00"
        if cost != 0:
            cost_text = formatNumber(cost)

        # format change
        change = balance - cost
        change_text = "00.00"
        if change > 0:
            change_text = formatNumber(change)
        else:
            change_text = "00.00"

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        machineWindow = curses.newwin(height, width, 0, self.stdscr.getmaxyx()[0]//4)
        for y in range(0, height):
            for x in range(0, width):
                try:
                    # color products when user selectes them
                    # coffee nr 1
                    if (selectedRows == 0) and y == coffe_1_cords['y'] and (x >= 5 and x <=21):
                        machineWindow.attron(curses.color_pair(1))
                     # coffee nr 2
                    elif (selectedRows == 1) and y == coffe_2_cords['y'] and (x >= 5 and x <=21):
                        machineWindow.attron(curses.color_pair(1))
                     # coffee nr 3
                    elif (selectedRows == 2) and y == coffe_3_cords['y'] and (x >= 5 and x <=21):
                        machineWindow.attron(curses.color_pair(1))
                    # turn off when no selection
                    else:
                        machineWindow.attroff(curses.color_pair(1))
                    
                    # print balance
                    if (x == balance_cords['x'] and y == balance_cords['y']) or (x == balance_cords['x']+1 and y == balance_cords['y']) or (x == balance_cords['x']+2 and y == balance_cords['y']) or (x == balance_cords['x']+3 and y == balance_cords['y']) or (x == balance_cords['x']+4 and y == balance_cords['y']):
                        offset = x-balance_cords['x']
                        machineWindow.addstr(formatNumber(balance)[offset])
                    # print cost of selected goods
                    elif (x == cost_cords['x'] and y == cost_cords['y']) or (x == cost_cords['x']+1 and y == cost_cords['y']) or (x == cost_cords['x']+2 and y == cost_cords['y']) or (x == cost_cords['x']+3 and y == cost_cords['y']) or (x == cost_cords['x']+4 and y == cost_cords['y']) or (x == cost_cords['x']+5 and y == cost_cords['y']):
                        offset = x-cost_cords['x']
                        if offset == 0:
                            machineWindow.addstr("-")
                        else:
                            machineWindow.addstr(cost_text[offset-1])
                    # print change
                    elif (x == change_cords['x'] and y == change_cords['y']) or (x == change_cords['x']+1 and y == change_cords['y']) or (x == change_cords['x']+2 and y == change_cords['y']) or (x == change_cords['x']+3 and y == change_cords['y']) or (x == change_cords['x']+4 and y == change_cords['y']):
                        offset = x-cost_cords['x']
                        machineWindow.addstr(change_text[offset-1])
                    # TODO: print diffrent labels from configuration, currently its hard-coded
                    elif (x == coffe_1_cords['x'] and y == coffe_1_cords['y']) or (x == coffe_1_cords['x']+1 and y == coffe_1_cords['y']) or (x == coffe_1_cords['x']+2 and y == coffe_1_cords['y']) or (x == coffe_1_cords['x']+3 and y == coffe_1_cords['y']) or (x == coffe_1_cords['x']+4 and y == coffe_1_cords['y']):
                        offset = x-coffe_1_cords['x']
                        machineWindow.addstr(coffe_1_cost[offset])
                    elif (x == coffe_2_cords['x'] and y == coffe_2_cords['y']) or (x == coffe_2_cords['x']+1 and y == coffe_2_cords['y']) or (x == coffe_2_cords['x']+2 and y == coffe_2_cords['y']) or (x == coffe_2_cords['x']+3 and y == coffe_2_cords['y']) or (x == coffe_2_cords['x']+4 and y == coffe_2_cords['y']):
                        offset = x-coffe_2_cords['x']
                        machineWindow.addstr(coffe_2_cost[offset])
                    elif (x == coffe_3_cords['x'] and y == coffe_3_cords['y']) or (x == coffe_3_cords['x']+1 and y == coffe_3_cords['y']) or (x == coffe_3_cords['x']+2 and y == coffe_3_cords['y']) or (x == coffe_3_cords['x']+3 and y == coffe_3_cords['y']) or (x == coffe_3_cords['x']+4 and y == coffe_3_cords['y']):
                        offset = x-coffe_3_cords['x']
                        machineWindow.addstr(coffe_3_cost[offset])
                    else:
                        # other symbols bg etc.
                        machineWindow.addstr(y, x, self.template[y][x])
                except curses.error as e:
                    pass
        # print selected goods aread
        if dispenser_1_count > 0:
            machineWindow.addstr(dispenser_1_cords['y'], dispenser_1_cords['x'], f"x{dispenser_1_count} black")
        if dispenser_2_count > 0:
            machineWindow.addstr(dispenser_2_cords['y'], dispenser_2_cords['x'], f"x{dispenser_2_count} cappucino")
        if dispenser_3_count > 0:
            machineWindow.addstr(dispenser_3_cords['y'], dispenser_3_cords['x'], f"x{dispenser_3_count} latte")
        return machineWindow

    # Data box used to print balance and put in machine info
    def renderAccountbox(self, height, maxwidth, putMode, nominal):
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        accountbox = curses.newwin(5, maxwidth, height+3, 0)
        accountbox.attron(curses.color_pair(2))

        if putMode:
            accountbox.addstr(f"Currently adding in {utils.moneyInNotesAsText(nominal)}| ")

        banknote_text = utils.moneyInNotesAsText(self.balance)
        accountbox.addstr(f"Your balance is: {self.balance}$ Coins: {banknote_text}")

        return accountbox

    # Help box used show keybinds
    def renderhelpbox(self, height, maxwidth, putMode):
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        helpbox = curses.newwin(5, maxwidth, height+4, 0)
        helpbox.attron(curses.color_pair(3))

        if putMode:
            helpbox.addstr(f"[1] [2] - put in/remove from | [3] [4] - decrease/increase nominal | [P] - exit mode | [Q]uit")
        else:
            helpbox.addstr("[ARROW UP] [ARROW DOWN] - navigate | [S]elect | [R]emove | [P]ut in coins | [A]pprove selection | [Q]uit")

        return helpbox

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

        selectedRow = 0
        selected = []
        coinsBalance = 00.00
        putMode = False
        # get the biggest nominal that we can put in to machine
        nominal = 5.0

        while True:
            machineWindow = self.renderMachine(height, width, selectedRow, selected, coinsBalance)
            machineWindow.refresh()

            accountboxWindow = self.renderAccountbox(height, cols, putMode, nominal)
            accountboxWindow.refresh()

            helpboxWindow = self.renderhelpbox(height, cols, putMode)
            helpboxWindow.refresh()

            self.stdscr.refresh()
            keybind = self.stdscr.getch()

            # normal mode
            if keybind == curses.KEY_UP and not putMode:
                if selectedRow-1 >= 0:
                    selectedRow-=1
            elif keybind == curses.KEY_DOWN and not putMode:
                if selectedRow+1 <= 2:
                    selectedRow+=1
            elif keybind == ord("s") and not putMode:
                if selectedRow <= 2:
                    if selected.count(self.items[selectedRow][0])+1 <= 9:
                        selected.append(self.items[selectedRow][0])
            elif keybind == ord("r") and not putMode:
                if selectedRow <= 2:
                    if selected.count(self.items[selectedRow][0])-1 >= 0:
                        selected.pop(selected.index(self.items[selectedRow][0]))
            elif keybind == ord("p"):
                if putMode:
                    putMode = False
                    selectedRow = 0
                else:
                    putMode = True
                    selectedRow = 3
            # when in put in money mode
            elif keybind == ord("2") and putMode:
                if coinsBalance+nominal <= 100:
                    if self.balance >= nominal:
                        coinsBalance+=nominal
                        self.balance-=nominal
            elif keybind == ord("1") and putMode:
                if coinsBalance-nominal >= 0:
                    coinsBalance-=nominal
                    self.balance+=nominal
            elif keybind == ord("4") and putMode:
                index = utils.BANKNOTES.index(nominal*100)
                if index-1 >= 0:
                    nominal = utils.BANKNOTES[index-1]/100
            elif keybind == ord("3") and putMode:
                index = utils.BANKNOTES.index(nominal*100)
                if index+1 < len(utils.BANKNOTES):
                    nominal = utils.BANKNOTES[index+1]/100
            # quit
            elif keybind == ord("q"):
                break