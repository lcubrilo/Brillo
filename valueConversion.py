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
    retVal = 1
    for index, potentialPrefix in enumerate(largerLetter):
        if unitOfMeasurement.startswith(potentialPrefix):
            retVal = largerAmount[index]; break

    for index, potentialPrefix in enumerate(smallerLetter):
        if unitOfMeasurement.startswith(potentialPrefix):
            retVal = smallerAmount[index]; break

    return retVal

def detectExponentAmount(unitOfMeasurement):
    if type(unitOfMeasurement) != str:
        raise Exception ("IJS: Should've been a string")
    if len(unitOfMeasurement) < 1:
        return 1
        #raise Exception ("IJS: Empty string")

    lastChar = unitOfMeasurement[-1]
    return int(lastChar) if lastChar.isdigit() else 1
    

# prefix -> no prefix -> different prefix
def removePrefix(value):
    (numericalValue, unitOfMeasurement) = value
    if len(unitOfMeasurement) == 1:
        return value
    if len(unitOfMeasurement) == 2 and unitOfMeasurement[-1].isdigit():
        return value

    numericalValue *= detectPrefixAmount(unitOfMeasurement) ** detectExponentAmount(unitOfMeasurement)
    unitOfMeasurement = unitOfMeasurement[1:]

    return (numericalValue, unitOfMeasurement)

def addPrefix(value, prefix):
    (numericalValue, unitOfMeasurement) = value

    numericalValue /= detectPrefixAmount(prefix) ** detectExponentAmount(unitOfMeasurement)

    return (numericalValue, prefix + unitOfMeasurement)

def convertPrefix(value, prefix, primitivePrecisionFix = True):
    num, unit = value
    value = (float(num), unit)
    normalized = removePrefix(value)
    retVal = addPrefix(normalized, prefix)
    if not primitivePrecisionFix:
        return retVal
    else:
        return fixPrecisionPrimitive(retVal)

def fixPrecisionPrimitive(val):
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
def testFunctions1():
    for test in generateTestUnits(20):
        test+="2" #for unit squared or cubed etc
        print("For {} got {}".format(test, detectPrefixAmount(test)))

def testFunctions2():
    print("\n(((((((((((((((((((((((((((((((((((((\nTESTING CONVERT TO BASE UNIT NO PREFIX")
    print("Original value\t  => \tConverted value\n========================================")
    values = generateTestValues(20)
    for test in values:
        (num, unit) = test; test = (num, unit+"2")
        (num, unit) = removePrefix(test); res = (num, unit)
        
        print("{:e} {} \t  => \t{:e} {}".format(test[0], test[1], res[0], res[1]))

def testFunctions3():
    print("\n(((((((((((((((((((((((((((((((((((((\nTESTING CONVERT FROM BASE UNIT ADDING PREFIX")
    print("        Original value\t   => \t  Converted value\n===================================================")
    values = generateTestValues(20, False)
    prefixes = generateTestUnits(20, units=False)
    for test, prefix in zip(values, prefixes):
        (num, unit) = test; test = (num, unit)
        (num, unit) = addPrefix(test, prefix); res = (num, unit)
        
        print("{:e} {}  \t\t=> \t{:e} {}".format(test[0], test[1], res[0], res[1]))

def testFunctions4():
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