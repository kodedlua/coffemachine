import curses
import curses.ascii
from loader import Loader
import utils
from utils import formatNumber
from time import sleep
import winsound

class Machine(object):
    def __init__(self, balance, stdscr, loader):
        self.balance = balance
        self.stdscr = stdscr
        self.template, self.config = loader.load()
        self.resources = self.config['resources']
        self.noti = [False, "blank", "blank", 2]
        self.items = []
        for key, item in self.config['inputdata'].items():
            if key.startswith("coffee"):
                self.items.append([key, item['cost'], item['recipe']])

    def renderMachine(self, height, width, selectedRows, selected, balance, putMode, setMode, nominal):
        # load all data and format it
        inputdata = self.config['inputdata']
        balance_cords = inputdata['balance']
        cost_cords = inputdata['cost']
        change_cords = inputdata['change']
        coffe_1_cords = {"x":inputdata['coffee-1']['x'], "y":inputdata['coffee-1']['y']}
        coffe_1_label = inputdata['coffee-1']['label']
        coffe_1_label_cords = {"x": inputdata['coffee-1']['x']-(2+len(coffe_1_label)), "y": inputdata['coffee-1']['y']}
        if not setMode: coffe_1_cost = formatNumber(self.items[0][1])
        else: coffe_1_cost = "--.--"
        coffe_2_cords = {"x":inputdata['coffee-2']['x'], "y":inputdata['coffee-2']['y']}
        coffe_2_label = inputdata['coffee-2']['label']
        coffe_2_label_cords = {"x": inputdata['coffee-2']['x']-(2+len(coffe_2_label)), "y": inputdata['coffee-2']['y']}
        if not setMode: coffe_2_cost = formatNumber(self.items[1][1])
        else: coffe_2_cost = "--.--"
        coffe_3_cords = {"x":inputdata['coffee-3']['x'], "y":inputdata['coffee-3']['y']}
        coffe_3_label = inputdata['coffee-3']['label']
        coffe_3_label_cords = {"x": inputdata['coffee-3']['x']-(2+len(coffe_3_label)), "y": inputdata['coffee-3']['y']}
        if not setMode: coffe_3_cost = formatNumber(self.items[2][1])
        else: coffe_3_cost = "--.--"
        dispenser_1_cords = inputdata['dispenser-1']
        dispenser_1_count = selected.count(self.items[0][0])
        dispenser_2_cords = inputdata['dispenser-2']
        dispenser_2_count = selected.count(self.items[1][0])
        dispenser_3_cords = inputdata['dispenser-3']
        dispenser_3_count = selected.count(self.items[2][0])

        # format cost
        cost = 0 + (self.items[0][1] * dispenser_1_count) + (self.items[1][1] * dispenser_2_count) + (self.items[2][1] * dispenser_3_count)
        self.cost = cost
        cost_text = "00.00"
        if cost != 0:
            cost_text = formatNumber(cost)

        # format change
        change = balance - cost
        self.change = change
        change_text = "00.00"
        if change > 0:
            change_text = formatNumber(change)
        else:
            change_text = "00.00"

        # format text near balance
        putText = ""
        if putMode: putText = f"←{utils.moneyInNotesAsText(nominal)}" 

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        machineWindow = curses.newwin(height, width, 0, self.stdscr.getmaxyx()[0]//4)
        machineWindow.erase()
        machineWindow.box()
        for y in range(1, height-1):
            for x in range(1, width-1):
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
                    elif (selectedRows == 3) and y == 17 and (x >= 36 and x <=40):
                        machineWindow.attron(curses.color_pair(1))
                    elif putMode and (x >= balance_cords['x'] and x <= balance_cords['x']+4) and y == balance_cords['y']:
                        machineWindow.attron(curses.color_pair(1))
                    # turn off when no selection
                    else:
                        machineWindow.attroff(curses.color_pair(1))
                    
                    # print balance
                    if (x >= balance_cords['x'] and x <= balance_cords['x']+4 and y == balance_cords['y']):
                        offset = x-balance_cords['x']
                        machineWindow.addstr(formatNumber(balance)[offset])
                    # print cost of selected goods
                    elif (x >= cost_cords['x'] and x <= cost_cords['x']+5 and y == cost_cords['y']):
                        offset = x-cost_cords['x']
                        if offset == 0:
                            machineWindow.addstr("-")
                        else:
                            machineWindow.addstr(cost_text[offset-1])
                    # print change
                    elif (x >= change_cords['x'] and x <= change_cords['x']+4 and y == change_cords['y']):
                        offset = x-cost_cords['x']
                        machineWindow.addstr(change_text[offset-1])
                    # print diffrent labels from configuration
                    elif (x >= coffe_1_label_cords['x'] and x <= coffe_1_label_cords['x']+len(coffe_1_label)-1 and y == coffe_1_label_cords['y']):
                        offset = x-coffe_1_label_cords['x']
                        machineWindow.addstr(coffe_1_label[offset])
                    elif (x >= coffe_2_label_cords['x'] and x <= coffe_2_label_cords['x']+len(coffe_2_label)-1 and y == coffe_2_label_cords['y']):
                        offset = x-coffe_2_label_cords['x']
                        machineWindow.addstr(coffe_2_label[offset])
                    elif (x >= coffe_3_label_cords['x'] and x <= coffe_3_label_cords['x']+len(coffe_3_label)-1 and y == coffe_3_label_cords['y']):
                        offset = x-coffe_3_label_cords['x']
                        machineWindow.addstr(coffe_3_label[offset])
                    # print costs of said products
                    elif (x >= coffe_1_cords['x'] and x <= coffe_1_cords['x']+4 and y == coffe_1_cords['y']):
                        offset = x-coffe_1_cords['x']
                        machineWindow.addstr(coffe_1_cost[offset])
                    elif (x >= coffe_2_cords['x'] and x <= coffe_2_cords['x']+4 and y == coffe_2_cords['y']):
                        offset = x-coffe_2_cords['x']
                        machineWindow.addstr(coffe_2_cost[offset])
                    elif (x >= coffe_3_cords['x'] and x <= coffe_3_cords['x']+4 and y == coffe_3_cords['y']):
                        offset = x-coffe_3_cords['x']
                        machineWindow.addstr(coffe_3_cost[offset])
                    elif (x >= 43 and x <= 49) and y == 12 and putMode:
                        offset = x-43
                        machineWindow.addstr(putText[offset])
                    else:
                        # other symbols bg etc.
                        machineWindow.addstr(y, x, self.template[y][x])
                except Exception as e:
                    print(f"Program thrown an exception! {e}")
                    pass
        # print selected goods aread
        if dispenser_1_count > 0:
            machineWindow.addstr(dispenser_1_cords['y'], dispenser_1_cords['x'], f"x{dispenser_1_count} black")
        if dispenser_2_count > 0:
            machineWindow.addstr(dispenser_2_cords['y'], dispenser_2_cords['x'], f"x{dispenser_2_count} cappucino")
        if dispenser_3_count > 0:
            machineWindow.addstr(dispenser_3_cords['y'], dispenser_3_cords['x'], f"x{dispenser_3_count} latte")
        machineWindow.refresh()
        return machineWindow

    # Data box used to print balance and put in machine info
    def renderUtilsBox(self, height, maxwidth, putMode, setMode):
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        accountbox = curses.newwin(3, 48, height+1, 17)
        helpbox = curses.newwin(5, maxwidth, height+4, 0)
        accountbox.box()
        if putMode:
            accountbox.addstr(0, 2, f"Twój portfel ({round(self.balance, 2)}$)")
            banknote_text = utils.moneyInNotesAsText(self.balance)
            accountbox.addstr(1, 1, f"{banknote_text}")
            helpbox.attron(curses.color_pair(2))
            helpbox.addstr(f"[↵] [↰] - włóź/wyjmij monete | [→] [←] - zwiększ/zmniejsz nominal | [P] przestań wrzucać | [Q] wyjdź")
        elif setMode:
            accountbox.addstr(0, 2, f"Twój portfel (--$)")
            banknote_text = "-"*46
            accountbox.addstr(1, 1, f"{banknote_text}")
            helpbox.attron(curses.color_pair(2))
            helpbox.addstr("[↑] [↓] nawiguj w góre/dół | [↵] zwiększ wartość | [↰] zmniejsz wartość | [S] przestań edytować | [Q] wyjdź")
        else:
            accountbox.addstr(0, 2, f"Twój portfel ({round(self.balance, 2)}$)")
            banknote_text = utils.moneyInNotesAsText(self.balance)
            accountbox.addstr(1, 1, f"{banknote_text}")
            helpbox.attron(curses.color_pair(2))
            helpbox.addstr("[↑] [↓] nawiguj w góre/dół | [↵] wybierz przedmiot | [↰] usuń przedmiot | [P] włóź monety | [S] edytuj właściwości | [Q] wyjdź")

        helpbox.refresh()
        accountbox.refresh()
        return accountbox, helpbox

    def renderAdminBox(self, setMode, selectedRow):
        adminbox = curses.newwin(12, 27, 3, 70)
        adminbox.box()
        adminbox.addstr(0, 2, "Właściwości")
        text = f"Woda: {self.resources['water']}ml"
        utils.addCenteredString(adminbox, 2, f"{text:15}")
        text = f"Mleko: {self.resources['milk']}ml"
        utils.addCenteredString(adminbox, 3, f"{text:15}")
        text = f"Ziarna kawy: {self.resources['coffee']}g"
        utils.addCenteredString(adminbox, 4, f"{text:15}")

        text = f"Zawartość portfela: {self.balance}$"
        utils.addCenteredString(adminbox, 6, f"{text:15}")

        text = f"Cena 1. produkt: {formatNumber(self.items[0][1])}$"
        utils.addCenteredString(adminbox, 7, f"{text:15}")
        text = f"Cena 2. produkt: {formatNumber(self.items[1][1])}$"
        utils.addCenteredString(adminbox, 8, f"{text:15}")
        text = f"Cena 3. produkt: {formatNumber(self.items[2][1])}$"
        utils.addCenteredString(adminbox, 9, f"{text:15}")
        if selectedRow == 80:
            adminbox.attron(curses.color_pair(1))
            text = f"Woda: {self.resources['water']}ml"
            utils.addCenteredString(adminbox, 2, f"{text:15}")
            adminbox.attroff(curses.color_pair(1))
        elif selectedRow == 81:
            adminbox.attron(curses.color_pair(1))
            text = f"Mleko: {self.resources['milk']}ml"
            utils.addCenteredString(adminbox, 3, f"{text:15}")
            adminbox.attroff(curses.color_pair(1))
        elif selectedRow == 82:
            adminbox.attron(curses.color_pair(1))
            text = f"Ziarna kawy: {self.resources['coffee']}g"
            utils.addCenteredString(adminbox, 4, f"{text:15}")
            adminbox.attroff(curses.color_pair(1))
        elif selectedRow == 83:
            adminbox.attron(curses.color_pair(1))
            text = f"Zawartość portfela: {self.balance}$"
            utils.addCenteredString(adminbox, 6, f"{text:15}")
            adminbox.attroff(curses.color_pair(1))
        elif selectedRow == 84:
            adminbox.attron(curses.color_pair(1))
            text = f"Cena 1. produkt: {formatNumber(self.items[0][1])}$"
            utils.addCenteredString(adminbox, 7, f"{text:15}")
            adminbox.attroff(curses.color_pair(1))
        elif selectedRow == 85:
            adminbox.attron(curses.color_pair(1))
            text = f"Cena 2. produkt: {formatNumber(self.items[1][1])}$"
            utils.addCenteredString(adminbox, 8, f"{text:15}")
            adminbox.attroff(curses.color_pair(1))
        elif selectedRow == 86:
            adminbox.attron(curses.color_pair(1))
            text = f"Cena 3. produkt: {formatNumber(self.items[2][1])}$"
            utils.addCenteredString(adminbox, 9, f"{text:15}")
            adminbox.attroff(curses.color_pair(1))
        adminbox.refresh()
        return adminbox

    def renderNotification(self, title, text, notiType):
        notificationWin = curses.newwin(5, 46, 8, 18)
        notificationWin.erase()
        notificationWin.box()
        notificationWin.addstr(0, 2, f"{title}")
        notificationWin.addstr(2, 1, f"{text}")
        if notiType == 2 or notiType == 3:
            notificationWin.attron(curses.color_pair(1))
            notificationWin.addstr(3, 21, f"Okej")
            notificationWin.attroff(curses.color_pair(1))
        notificationWin.refresh()
        return notificationWin


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
        setMode = False
        # the biggest nominal that we can put in to machine TODO: try to establish biggest nominal possible after looking at amount user inputed
        nominal = 5.0

        while True:
            machineWindow = self.renderMachine(height, width, selectedRow, selected, coinsBalance, putMode, setMode, nominal)
            utilsWindow = self.renderUtilsBox(height, cols, putMode, setMode)
            adminWindow = self.renderAdminBox(setMode, selectedRow)
            if self.noti[0] : notiWindow = self.renderNotification(self.noti[1], self.noti[2], self.noti[3])

            self.stdscr.refresh()
            keybind = self.stdscr.getch()
            # navigation
            if keybind == curses.KEY_UP and not putMode and not self.noti[0] and not setMode:
                if selectedRow-1 >= 0:
                    selectedRow-=1
                else:
                    winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
            elif keybind == curses.KEY_DOWN and not putMode and not self.noti[0] and not setMode:
                if selectedRow+1 <= 3:
                    selectedRow+=1
                else:
                    winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
            # navigation when in admin mode
            elif keybind == curses.KEY_UP and not putMode and not self.noti[0] and setMode:
                if selectedRow-1 >= 80:
                    selectedRow-=1
                else:
                    winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
            elif keybind == curses.KEY_DOWN and not putMode and not self.noti[0] and setMode:
                if selectedRow+1 <= 86:
                    selectedRow+=1
                else:
                    winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
            # normal mode enter
            elif (keybind == curses.KEY_ENTER or keybind == 10 or keybind == 13) and not putMode and not self.noti[0] and not setMode:
                if selectedRow <= 2:
                    if selected.count(self.items[selectedRow][0])+1 <= 2:
                        print(f"MENU | Added {self.items[selectedRow][0]} to selection")
                        selected.append(self.items[selectedRow][0])
                else:
                    if len(selected) > 0:
                        if coinsBalance >= self.cost:
                            inputdata = self.config['inputdata']
                            toDispense = []
                            for select in selected:
                                water = inputdata[select]['recipe'][0]
                                milk = inputdata[select]['recipe'][1]
                                coffee = inputdata[select]['recipe'][2]
                                if water < self.resources['water'] and milk < self.resources['milk'] and coffee < self.resources['coffee']:
                                    toDispense.append(select)
                                    self.resources['water'] -= water
                                    self.resources['milk'] -= milk
                                    self.resources['coffee'] -= coffee
                                else:
                                    selectedRow = 99
                                    utils.showNotification(self, "Maszyna", "Brak składników do wykonania zamówienia", 2)
                            self.balance+=self.change
                            coinsBalance=0
                            selected.clear()
                            selectedRow = 99
                            if selected == toDispense:
                                utils.showNotification(self, "Maszyna", f"Zakonczono prace! Twoja kawa: {utils.coffeeAsText(toDispense)}", 3)
                            else:
                                utils.showNotification(self, "Maszyna", f"Nie całe zamówienie zrealizowane! Kawa: {utils.coffeeAsText(toDispense)}", 3)
                        else:
                            selectedRow = 99
                            utils.showNotification(self, "Maszyna", "Nie wystarczająca ilość środków", 2)
                    else:
                        selectedRow = 99
                        utils.showNotification(self, "Maszyna", "Zamówienie puste", 2)
            # notifcation enter
            elif (keybind == curses.KEY_ENTER or keybind == 10 or keybind == 13) and self.noti[0]:
                if self.noti[3] == 2 or self.noti[3] == 3:
                    self.noti[0] = False
                    selectedRow = 0
            # put mode enter
            elif (keybind == curses.KEY_ENTER or keybind == 10 or keybind == 13) and not self.noti[0] and putMode and not setMode:
                if coinsBalance+nominal <= 100:
                    if self.balance >= nominal:
                        coinsBalance+=nominal
                        self.balance-=nominal
            # admin mode enter
            elif (keybind == curses.KEY_ENTER or keybind == 10 or keybind == 13) and not self.noti[0] and not putMode and setMode:
                if selectedRow == 80:
                    self.resources['water'] += 50
                elif selectedRow == 81:
                    self.resources['milk'] += 25
                elif selectedRow == 82:
                    self.resources['coffee'] += 10
                elif selectedRow == 83:
                    self.balance += 5
                elif selectedRow == 84:
                    self.items[0][1] += 0.05
                elif selectedRow == 85:
                    self.items[1][1] += 0.05
                elif selectedRow == 86:
                    self.items[2][1] += 0.05
            # normal mode backspace
            elif (keybind == curses.KEY_BACKSPACE or keybind == 127 or keybind == ord("\b") or keybind == curses.ascii.DEL) and not putMode and not self.noti[0] and not setMode:
                if selectedRow <= 2:
                    if selected.count(self.items[selectedRow][0])-1 >= 0:
                        selected.pop(selected.index(self.items[selectedRow][0]))
            # put mode backspace
            elif (keybind == curses.KEY_BACKSPACE or keybind == 127 or keybind == ord("\b") or keybind == curses.ascii.DEL) and putMode and not self.noti[0] and not setMode:
                if coinsBalance-nominal >= 0:
                    coinsBalance-=nominal
                    self.balance+=nominal
            # admin mode backspace
            elif (keybind == curses.KEY_BACKSPACE or keybind == 127 or keybind == ord("\b") or keybind == curses.ascii.DEL) and not putMode and not self.noti[0] and setMode:
                if selectedRow == 80:
                    self.resources['water'] -= 50
                elif selectedRow == 81:
                    self.resources['milk'] -= 25
                elif selectedRow == 82:
                    self.resources['coffee'] -= 10
                elif selectedRow == 83:
                    self.balance -= 5
                elif selectedRow == 84:
                    self.items[0][1] -= 0.05
                elif selectedRow == 85:
                    self.items[1][1] -= 0.05
                elif selectedRow == 86:
                    self.items[2][1] -= 0.05
            elif keybind == ord("p") and not self.noti[0] and not setMode:
                if putMode:
                    putMode = False
                    selectedRow = 0
                else:
                    putMode = True
                    selectedRow = 99
            elif keybind == ord("s") and not self.noti[0] and not putMode:
                if setMode:
                    setMode = False
                    selectedRow = 0
                else:
                    setMode = True
                    selectedRow = 80
            elif keybind == curses.KEY_RIGHT and putMode and not self.noti[0] and not setMode:
                index = utils.BANKNOTES.index(nominal*100)
                if index-1 >= 0:
                    nominal = utils.BANKNOTES[index-1]/100
            elif keybind == curses.KEY_LEFT and putMode and not self.noti[0] and not setMode:
                index = utils.BANKNOTES.index(nominal*100)
                if index+1 < len(utils.BANKNOTES):
                    nominal = utils.BANKNOTES[index+1]/100
            # quit
            elif keybind == ord("q"):
                break

