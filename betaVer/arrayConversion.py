import valueConversion

def convertPrefix(array, unit, prefix):
    res = []
    for el in array:
        tmp =  valueConversion.convertPrefix((el, unit), prefix)
        res.append(tmp)
    return [value[0] for value in res], res[1][1]


def testFunctions1():
    array = valueConversion.generateTestNumbers(20)
    unit = valueConversion.generateTestUnits(1)[0]
    prefix = valueConversion.generateTestUnits(1, True, False)[0]

    print("++++++++++++++++++++++++++\nWe started with this")
    for el in array:
        print("\t {:e} {}".format(el, unit))

    res, newUnit = convertPrefix(array, unit, prefix)
    print("We ended with this")
    for el in res:
        print("\t {:e} {}".format(el, newUnit))

testFunctions1()