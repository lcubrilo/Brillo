"""
This package is to be used for converting the order of magnitude of units of measurement
"""
# Global variables
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

def detectPrefixAmount(unitOfMeasurement):
    for index, potentialPrefix in enumerate(largerLetter):
        if unitOfMeasurement.startswith(potentialPrefix):
            return largerAmount[index]

    for index, potentialPrefix in enumerate(smallerLetter):
        if unitOfMeasurement.startswith(potentialPrefix):
            return smallerAmount[index]
            
    return 1


def removePrefix(value):
    (numericalValue, unitOfMeasurement) = value

    numericalValue *= detectPrefixAmount(unitOfMeasurement)
    unitOfMeasurement = unitOfMeasurement[1:]

    return (numericalValue, unitOfMeasurement)

def addPrefix(value, prefix):
    (numericalValue, unitOfMeasurement) = value

    numericalValue /= detectPrefixAmount(prefix)

    return (numericalValue, prefix + unitOfMeasurement)

def convertPrefix(value, prefix):
    normalized = removePrefix(value)
    return addPrefix(normalized, prefix)

def getValue(string, valueName, terminator = "\n", suffix = ": ", subfunction = False):
    startIndex = string.index(valueName) +  len(valueName + suffix)
    terminatorIndex = string.index(terminator, startIndex) if terminator != None else len(string)

    numericData = string[startIndex : terminatorIndex]
    unitOfMeasurement = getValue(valueName, "[", terminator="]", suffix="", subfunction=True) if not subfunction else ""

    return (numericData, unitOfMeasurement)

# tuple to str & vice versa
def tuple2str(value):
    return str(value[0]) + " " + str(value[1])

def str2tuple(value):
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
    from random import random, uniform
    return [random()*uniform(-60, 80) for i in range(sampleSize)]

def generateTestValues(sampleSize, prefixes=True):
    units = generateTestUnits(sampleSize, prefixes)
    nums = generateTestNumbers(sampleSize)

    return list(zip(nums, units))

# Test runs 
def testFuctions1():
    for test in generateTestUnits(20):
        print("For {} got {}".format(test, detectPrefixAmount(test)))
#testFuctions1()

def testFunctions2():
    print("\n(((((((((((((((((((((((((((((((((((((\nTESTING CONVERT TO BASE UNIT NO PREFIX")
    print("Original value\t  => \tConverted value\n========================================")
    values = generateTestValues(20)
    for test in values:
        (num, unit) = test; test = (num, unit)
        (num, unit) = removePrefix(test); res = (num, unit)
        
        print("{:e} {} \t  => \t{:e} {}".format(test[0], test[1], res[0], res[1]))
#testFunctions2()

def testFunctions3():
    print("\n(((((((((((((((((((((((((((((((((((((\nTESTING CONVERT FROM BASE UNIT ADDING PREFIX")
    print("        Original value\t   => \t  Converted value\n===================================================")
    values = generateTestValues(20, False)
    prefixes = generateTestUnits(20, units=False)
    for test, prefix in zip(values, prefixes):
        (num, unit) = test; test = (num, unit)
        (num, unit) = addPrefix(test, prefix); res = (num, unit)
        
        print("{:e} {}  \t\t=> \t{:e} {}".format(test[0], test[1], res[0], res[1]))
#testFunctions3()

def testFunctions4():
    print("\n(((((((((((((((((((((((((((((((((((((\nTESTING CONVERT FROM ONE PREFIX TO ANOTHER CHANGING PREFIX")
    print("        Original value\t  => \t  Converted value\n===================================================")
    values = generateTestValues(20)
    prefixes = generateTestUnits(20, units=False)
    for test, prefix in zip(values, prefixes):
        (num, unit) = test; test = (num, unit)
        (num, unit) = convertPrefix(test, prefix); res = (num, unit)
        
        print("{:e} {} \t  => \t{:e} {}".format(test[0], test[1], res[0], res[1]))


testFunctions2()
testFunctions3()
testFunctions4()
#print(generateTestValues(20))