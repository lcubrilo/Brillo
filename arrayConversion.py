import valueConversion
from improvedFunctions import getValue

def adapter_divideByValue(paket, oldCol, newCol, val, shouldIDelete=False):
    """
    Divides elements of a specific column by a given value within a brlopack object.

    Args:
        paket (brlopack): The brlopack object containing files and tables.
        oldCol (str): The name of the existing column to be divided.
        newCol (str): The name of the new column to store the result.
        val (tuple): A tuple containing the numerical value and unit to divide by.
        shouldIDelete (bool, optional): If True, the old column will be deleted. Defaults to False.
    """

    (num, un) = val
    
    files = paket.tellMeFiles()
    for file in files:
        for table in paket.tellMeTablesInFile(file):
            paket.data[file][table][newCol] = [el/val for el in paket.data[file][table][oldCol]]
            if shouldIDelete: 
                del paket.data[file][table][oldCol]

def divideByValue(array, unit, value):
    """
    Divides an array by a given value and returns the result with an updated unit.

    Args:
        array (list): The input array of numerical values.
        unit (str): The unit of the input values.
        value (tuple): A tuple containing the numerical value and unit to divide by.

    Returns:
        tuple: A tuple containing the resulting array and the updated unit.
    """
    (num, un) = value
    unit += "/"+un

    res = []
    for el in array:
        res.append(el/num)
    return res, unit

def adapter_ConvertPrefix(paket, oldCol, newCol, otherArgs=None):
    """
    Adapts the conversion of prefixes for columns within a brlopack object.

    Calls the function `adapterConvertPrefix`.

    Args:
        paket (brlopack): The brlopack object containing files and tables.
        oldCol (str): The name of the existing column with the original prefix.
        newCol (str): The name of the new column with the desired prefix.
        otherArgs (optional): Additional arguments. Defaults to None.
    """
    for file in paket.tellMeFiles():
        for table in paket.tellMeTablesInFile(file):
            temporary = adapterConvertPrefix(paket.data[file][table][oldCol], oldCol, newCol)
            paket.data[file][table][newCol] = temporary[0]

def adapterConvertPrefix(array, oldColNam, newColNam):
    """
    Converts the prefixes of the units in an array based on the old and new column names.

    Calls the function `getValue` from `improvedFunctions` and refers to global variables in `valueConversion`.

    Args:
        array (list): The input array of numerical values.
        oldColNam (str): The name of the existing column with the original prefix.
        newColNam (str): The name of the new column with the desired prefix.

    Returns:
        tuple: A tuple containing the resulting array and the updated unit.
    """
    unit = getValue(oldColNam, "[", terminator="]", suffix="", subfunction=True)
    newUnit = getValue(newColNam, "[", terminator="]", suffix="", subfunction=True)

    # TODO add check if suffixes match at least one char and raise exception

    for letter in valueConversion.smallerLetter + valueConversion.largerLetter:
        if newUnit.startswith(letter):
            prefix = letter
            return convertPrefix(array, unit, prefix)
    
    raise Exception("IJS: Couldn't recognize unit prefix.")

def convertPrefix(array, unit, prefix):
    """
    Converts the prefixes of units in an array and returns the result.

    Refers to the `convertPrefix` function in the `valueConversion` module.

    Args:
        array (list): The input array of numerical values.
        unit (str): The original unit of the values.
        prefix (str): The desired prefix for the new unit.

    Returns:
        tuple: A tuple containing the resulting array and the updated unit.
    """
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