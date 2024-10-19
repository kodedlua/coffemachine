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