import valueConversion
from improvedFunctions import getValue

def adapter_divideByValue(paket, oldCol, newCol, val, shouldIDelete=False):
    (num, un) = val
    
    files = paket.tellMeFiles()
    for file in files:
        for table in paket.tellMeTablesInFile(file):
            paket.data[file][table][newCol] = [el/val for el in paket.data[file][table][oldCol]]
            if shouldIDelete: del paket.data[file][table][oldCol]

def divideByValue(array, unit, value):
    (num, un) = value
    unit += "/"+un

    res = []
    for el in array:
        res.append(el/num)
    return res, unit

def adapter_ConvertPrefix(paket, oldCol, newCol):
    for file in paket.tellMeFiles():
        for table in paket.tellMeTablesInFile(file):
            temporary = adapterConvertPrefix(paket.data[file][table][oldCol], oldCol, newCol)
            paket.data[file][table][newCol] = temporary[0]

def adapterConvertPrefix(array, oldColNam, newColNam):
    
    unit = getValue(oldColNam, "[", terminator="]", suffix="", subfunction=True)
    newUnit = getValue(newColNam, "[", terminator="]", suffix="", subfunction=True)

    # TODO add check if suffixes match at least one char and raise exception

    for letter in valueConversion.smallerLetter + valueConversion.largerLetter:
        if newUnit.startswith(letter):
            prefix = letter
            return convertPrefix(array, unit, prefix)
    
    raise Exception("IJS: Couldn't recognize unit prefix.")

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

def testFunctions2():
    array = valueConversion.generateTestNumbers(20)
    oldColNam = "V+ [V]"
    newColNam = "V+ [mV]"

    print("++++++++++++++++++++++++++\nWe started with this:", oldColNam)
    for el in array:
        print("\t {:e}".format(el))
    

    newArray = adapterConvertPrefix(array, oldColNam, newColNam)[0]
    print("++++++++++++++++++++++++++\nWe ended with this:", newColNam)
    for el in newArray:
        print("\t {:e}".format(el))

if __name__ == "__main__":
    testFunctions2()