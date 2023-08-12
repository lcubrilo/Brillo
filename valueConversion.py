"""
This package is to be used for converting the order of magnitude of units of measurement
"""
# Global variables
# TODO check for number of real digits, save it and use it to round off any precision errors
# numDig = len(str(num).replace("0", " " ).strip())
# Alternatively check for repeating 99999s and x00000y, where y is just one digit
exponents = [2, 3, 6, 9, 12]#[1, 2, 3, 6, 9, 12]

smallerLetter = [ # ordered by magnitude (small to smallest)
        # removed for symmetry sake of deka "d",  # deci
        "c", # centi
        "m", # mili
        "u", # micro
        "n", # nano
        "p" # pico
    ]
smallerAmount = [10**-exp for exp in exponents]

largerLetter = [ # ordered by magnitude (large to largest)
        # it's annoying to have a two letter exception to the rule "da", # deka
        "h", # hecto
        "k", # kilo
        "M", # mega
        "G", # giga
        "T", # terra
    ]
largerAmount = [10**exp for exp in exponents]

# Connect global variables together
def detectPrefixAmount(unitOfMeasurement):
    """
    Fetches global data defined in valueConversion.py - how much is a kilo, mega, mili etc.

    Args:
        unitOfMeasurement (str): The unit of measurement with a prefix (e.g., "k" for kilo).

    Returns:
        float: The numerical value of the prefix (e.g., 1000 for "k").
    """
    retVal = 1
    for index, potentialPrefix in enumerate(largerLetter):
        if unitOfMeasurement.startswith(potentialPrefix):
            retVal = largerAmount[index]; break

    for index, potentialPrefix in enumerate(smallerLetter):
        if unitOfMeasurement.startswith(potentialPrefix):
            retVal = smallerAmount[index]; break

    return retVal

def detectExponentAmount(unitOfMeasurement):
    """
    Determines the exponent value in the given unit of measurement (e.g. if something is a kilogram, meter squared, cm qubed etc)
    Note: Assumes single-digit exponents of units by looking at the last char.
    Note 2: Doesn't see if exponents appear for more than one unit, only sees it for the last occurence.

    Args:
        unitOfMeasurement (str): The unit of measurement with an exponent.

    Returns:
        int: The exponent value if found, otherwise 1.
    """
    if type(unitOfMeasurement) != str:
        raise Exception ("IJS: Should've been a string")
    if len(unitOfMeasurement) < 1:
        return 1
        #raise Exception ("IJS: Empty string")

    lastChar = unitOfMeasurement[-1]
    return int(lastChar) if lastChar.isdigit() else 1
    

# prefix -> no prefix -> different prefix
def removePrefix(value):
    """
    Converts a value to its SI base unit without prefixes. 
    Note: Now works properly for a meter squared or cubic centimeter (single digit exponents)
    
    Args:
        value (tuple): A tuple containing the numerical value and the unit of measurement.

    Returns:
        tuple: The value converted to its base SI unit.
    """
    (numericalValue, unitOfMeasurement) = value
    if len(unitOfMeasurement) == 1:
        return value
    if len(unitOfMeasurement) == 2 and unitOfMeasurement[-1].isdigit():
        return value

    numericalValue *= detectPrefixAmount(unitOfMeasurement) ** detectExponentAmount(unitOfMeasurement)
    unitOfMeasurement = unitOfMeasurement[1:]

    return (numericalValue, unitOfMeasurement)

def addPrefix(value, prefix):
    """
    Assuming a value is in its base SI value (no prefixes) adds a given prefix. 
    If assumption incorrect, either use `removePrefix()` first or let `convertPrefix()` do it for you.
    Note: Now works properly for a meter squared or cubic centimeter (single digit exponents)
    
    Args:
        value (tuple): A tuple containing the numerical value and the unit of measurement.
        prefix (str): The prefix to add to the unit.

    Returns:
        tuple: The value with the added prefix.
    """
    (numericalValue, unitOfMeasurement) = value

    numericalValue /= detectPrefixAmount(prefix) ** detectExponentAmount(unitOfMeasurement)

    return (numericalValue, prefix + unitOfMeasurement)

def convertPrefix(value, prefix, primitivePrecisionFix = True):
    """
    Converts to desired prefix (first to base then to inputted prefix)

    Args:
        value (tuple): A tuple containing the numerical value and the unit of measurement.
        prefix (str): The desired prefix to convert to.
        primitivePrecisionFix (bool, optional): Whether to apply a primitive precision fix to avoid ugly numbers like 0.0000001 or 9.99999

    Returns:
        tuple: The value converted to the desired prefix.
    """
    num, unit = value
    value = (float(num), unit)
    normalized = removePrefix(value)
    retVal = addPrefix(normalized, prefix)
    if not primitivePrecisionFix:
        return retVal
    else:
        return fixPrecisionPrimitive(retVal)

def fixPrecisionPrimitive(val):
    """
    Seeks where some decimals could be rounded off (such as 0.41999 or 3.0004).
    (they become 0.42 and 3.0 respectively)
    Note: Will trigger only if it sees 3 adjacent 9s or 0s.

    Args:
        val (tuple): A tuple containing the numerical value and the unit of measurement.

    Returns:
        tuple: The value with precision fixed.
    """
    num, unit = val
    numStr = str(num); numFlo = float(num)
    susSituation = ["999", "000"]
    for sus in susSituation:
        if numStr.__contains__(sus):
            susIndex = numStr.find(sus)
            pointIndex = numStr.find(".")
            deltaIndex = susIndex - pointIndex + 1
            numFlo = round(numFlo, deltaIndex)
            break
    return (num, unit) if numFlo == 0 else (numFlo, unit) 

val = (3.229999678, "cm")
res = fixPrecisionPrimitive(val)

# tuple to str & vice versa
def tuple2str(value):
    """
    Converts our value (a tuple of number and string for unit) into a string for printing.

    Args:
        value (tuple): A tuple containing the numerical value and the unit of measurement.

    Returns:
        str: The value represented as a string.
    """
    return str(value[0]) + " " + str(value[1])

def str2tuple(value):
    """
    Converts our string into a value (a tuple of number and string for unit).
    
    Args:
        value (str): The value represented as a string.

    Returns:
        tuple: A tuple containing the numerical value and the unit of measurement.
    
    """
    
    # Regex expression for detecting all numbers
    import re
    number = re.findall(r'[.\d]+', value)

    # You want only one number to pop out (expected format eg '45.3kg')
    if len(number) != 1:
        raise Exception("Cudnovate stvari se zbivaju. lol.")
    number = number[0]

    unit = value[len(number):]

    return (float(number), unit)

#print(str2tuple("345.3str"))

# Test cases generation
def generateTestUnits(sampleSize=None, prefixes=True, units=True):
    """
    Generates a list of test units for testing purposes.

    Args:
        sampleSize (int, optional): The number of test units to generate. If None, all possible combinations are returned.
        prefixes (bool, optional): Whether to include unit prefixes in the test units.
        units (bool, optional): Whether to include base units in the test units.

    Returns:
        list: A list of test units as strings.
    """
    testPrefixes = smallerLetter + largerLetter if prefixes else [""]

    testUnits = ["s", "m", "g", "A", "K", "mol", "cd", "Hz", "rad", "sr", "N", "Pa", "J", "W", "C", "V", "Wb", "T", "F", "ohm", "S", "H", "C", "lm", "lx", "Bq", "Gy", "Sv", "kat", "L", "bar", "t", "Pa", "Mx", "rad", "eV", "Wh", "cal", "ft", "inch", "ppi", "bit"] if units else [""]

    allTests = [prefix+unit for prefix in testPrefixes for unit in testUnits]

    if sampleSize == None:
        return allTests   

    from random import sample
    try:
        return sample(allTests, k=sampleSize)
    except:
        retVal = allTests + generateTestUnits(sampleSize-len(allTests), prefixes, units)
        return sample(retVal, k=len(retVal))

def generateTestNumbers(sampleSize):
    """
    Generates a list of random test numbers for testing purposes.

    Args:
        sampleSize (int): The number of test numbers to generate.

    Returns:
        list: A list of random floating-point numbers.
    """
    from random import random, uniform
    return [random()*uniform(-60, 80) for i in range(sampleSize)]

def generateTestValues(sampleSize, prefixes=True):
    """
    Generates a list of test values (numbers with units) for testing purposes.

    Args:
        sampleSize (int): The number of test values to generate.
        prefixes (bool, optional): Whether to include unit prefixes in the test values.

    Returns:
        list: A list of test values as tuples of numbers and units.
    """
    units = generateTestUnits(sampleSize, prefixes)
    nums = generateTestNumbers(sampleSize)

    return list(zip(nums, units))

# Test runs 
def testFunctions1():
    """
    Test function to validate the behavior of detecting prefixes.
    Prints the test cases and results to the console.
    """
    for test in generateTestUnits(20):
        test+="2" #for unit squared or cubed etc
        print("For {} got {}".format(test, detectPrefixAmount(test)))

def testFunctions2():
    """
    Test function to validate the behavior of converting to the base unit.
    Prints the test cases and results to the console.
    """
    print("\n(((((((((((((((((((((((((((((((((((((\nTESTING CONVERT TO BASE UNIT NO PREFIX")
    print("Original value\t  => \tConverted value\n========================================")
    values = generateTestValues(20)
    for test in values:
        (num, unit) = test; test = (num, unit+"2")
        (num, unit) = removePrefix(test); res = (num, unit)
        
        print("{:e} {} \t  => \t{:e} {}".format(test[0], test[1], res[0], res[1]))

def testFunctions3():
    """
    Test function to validate the behavior of converting from the base unit, adding a prefix.
    Prints the test cases and results to the console.
    """
    print("\n(((((((((((((((((((((((((((((((((((((\nTESTING CONVERT FROM BASE UNIT ADDING PREFIX")
    print("        Original value\t   => \t  Converted value\n===================================================")
    values = generateTestValues(20, False)
    prefixes = generateTestUnits(20, units=False)
    for test, prefix in zip(values, prefixes):
        (num, unit) = test; test = (num, unit)
        (num, unit) = addPrefix(test, prefix); res = (num, unit)
        
        print("{:e} {}  \t\t=> \t{:e} {}".format(test[0], test[1], res[0], res[1]))

def testFunctions4():
    """
    Test function to validate the behavior of converting from one prefix to another.
    Prints the test cases and results to the console.
    """
    print("\n(((((((((((((((((((((((((((((((((((((\nTESTING CONVERT FROM ONE PREFIX TO ANOTHER CHANGING PREFIX")
    print("        Original value\t  => \t  Converted value\n===================================================")
    values = generateTestValues(20)
    prefixes = generateTestUnits(20, units=False)
    for test, prefix in zip(values, prefixes):
        (num, unit) = test; test = (num, unit)
        (num, unit) = convertPrefix(test, prefix); res = (num, unit)
        
        print("{:e} {} \t  => \t{:e} {}".format(test[0], test[1], res[0], res[1]))

if __name__ == "__main__2":
    testFunctions1()
    testFunctions2()
    testFunctions3()
    testFunctions4()
    #print(generateTestValues(20))