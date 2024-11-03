import curses
import winsound

def formatNumber(cost: int) -> str:
    return "%02d" % (cost) + str('{0:.2f}'.format(float(cost%1))).removeprefix("0")

BANKNOTES = [1000, 500, 100, 25, 10, 5, 1]

# using greedy change alghorithm for now, TODO: dynamic approach to the problem, if even possible on larger scale
def moneyInNotesAsList(amount:int, notes:list=BANKNOTES) -> list:
    K = [0 for x in range(len(notes))]
    i = 0
    while amount > 0:
        K[i] = amount // notes[i]
        amount = amount % notes[i]
        i += 1
    return K

def moneyInNotesAsText(amount: int, notes: list=BANKNOTES) -> str:
    realAmount = int(amount*100)
    solution = moneyInNotesAsList(realAmount, notes)

    text = []
    for i, banknote in enumerate(notes):
        if solution[i] > 0:
            if banknote > 99:
                for x in range(solution[i]): text.append(f"{banknote//100}$ ")
            else:
                for x in range(solution[i]): text.append(f"{banknote}¢ ")
    return "".join(text)

def showNotification(self, title: str, text: str, nType: int):
    if nType == 2:
        winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
    else:
        winsound.PlaySound("SystemQuestion", winsound.SND_ASYNC)
    self.noti = [True, title, text, nType]

def addCenteredString(window:curses.window, height: int, text: str):
    _h, width = window.getmaxyx()
    window.addstr(height, width//2-len(text)//2, text)

def coffeeAsText(toDispense: list) -> str:
    text = []

    for i, coffee in enumerate(toDispense):
        if coffee == "coffee-1":
            text.append("🥤")
        elif coffee == "coffee-2":
            text.append("☕")
        elif coffee == "coffee-3":
            text.append("🧋")
    return "".join(text)
