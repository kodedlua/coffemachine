def convertCost(cost) -> str:
    return "%02d" % (cost) + str('{0:.2f}'.format(float(cost%1))).removeprefix("0")

STATE_SELECTED_1 = 1
STATE_SELECTED_2 = 2
STATE_SELECTED_3 = 3