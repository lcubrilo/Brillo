import pandas as pd
import numpy as np

# Helper functions
def fileToStr(fileName):
    print("Loading file {}".format(fileName))
    lines = ""
    with open(fileName) as f:
        for line in f:
            lines += line

    return lines

def sectionTheFile(lines, printSummary):
    sections = lines.split("Table ")

    title = sections[0].strip()

    summarySection = sections[2]
    summaryLines = summarySection.split("\n")

    if printSummary:
        print("Title: {}\n==============\nSummary table:".format(title))
        for line in summaryLines:
            print(line)
    
    return sections[3:]

currentTableName = None

def loadSection(section, shouldPrint=False, sectionName="Contour "):
    # Some preprocessing
    lastLine = "Measurement Status: 0\n"
    index = section.index(lastLine) + len(lastLine)
    
    dataBeforeTable = section[:index]
    
    global currentTableName; currentTableName = sectionName + dataBeforeTable[:dataBeforeTable.index("\n")]
    
    # AFAIK the only useful data we need are area and thickness. TODO check if we need others
    area = getValue(dataBeforeTable, "Area [mm2]")
    thickness = getValue(dataBeforeTable, "Thickness [nm]") # TODO doesn't get unit of measurement SADA GA DOBIJA, ZASTO
    #thickness = float(thickness[0]) # That perhaps answers the question above. Why do this?

    # Now get the table from the string - MAIN PART
    table = section.strip()[index:].split("\n")
    for i, line in enumerate(table):
        table[i] = table[i].strip().split("\t")
        if i == 0: continue
        for j, cell in enumerate(table[i]):
            table[i][j] = float(table[i][j])

    # Separate column names
    columnNames = table[0]

    dataFrame = pd.DataFrame(
        data = np.array(table[1:]), # TODO why np array and not list
        columns=columnNames
        )

    if shouldPrint:
        print(dataFrame)

    #dataFrame["INTERESTING CONSTANTS"] = [area, thickness]
    interestingConstants = {"area":area, "thickness":thickness}
    return dataFrame, interestingConstants

def getValue(string, valueName, terminator = "\n", suffix = ": ", subfunction = False):
    startIndex = string.index(valueName) +  len(valueName + suffix)
    terminatorIndex = string.index(terminator, startIndex) if terminator != None else len(string)

    numericData = string[startIndex : terminatorIndex]
    if subfunction:
        return numericData

    unitOfMeasurement = getValue(valueName, "[", terminator="]", suffix="", subfunction=True)

    return (float(numericData), unitOfMeasurement)

# Main function
def load_aixACCTFile(fileName, printSummary = False):
    if not fileName.endswith(".dat"): raise Exception("Expected a .dat file of aixACCT.")
    lines = fileToStr(fileName)

    sections = sectionTheFile(lines, printSummary)

    dataFrameList = {}; constantsList ={}
    for section in sections:
        tmpDataFrame, constants = loadSection(section)
        dataFrameList[currentTableName] = tmpDataFrame
        constantsList[currentTableName] = constants
    
    return dataFrameList, constantsList

def load_probostatFile(fileName):
    if not fileName.endswith(".csv"): raise Exception("Expected a .csv file of Probostat.")
    f = open(fileName, "r") # open the file
    matrix = [] # get an empty table ready
    x_axis = None
    for line in f: # go line by line in file - that is gonna become our rows in table
        if not x_axis and line.startswith(";Assigned to Axis: "):
            index = line.find(";Assigned to Axis: ") + len(";Assigned to Axis: ")
            x_axis = line[index:].strip()
        if line == "\n": continue # skip empty rows; "\n" means "newline"
        tmpArr = line.split(";") # separate values by the ";" character and store in a temporary array
        if len(tmpArr) > 1: tmpArr=tmpArr[1:] # they always had the first one empty, delete it
        if len(tmpArr) == 1: continue # if it has just one element it is pre-table bullshit
        if not tmpArr[0].isdigit(): # this only happens in the header row (where names of columns are)
            n = len("X data for ")
            for i in range(1, len(tmpArr)):
                tmpArr[i] = tmpArr[i][n:] # this removes "X data for " from beginning of column name
            tmpArr = [tmpArr[i] for i in range(len(tmpArr)) if i%2==0 or i==1]
            tmpArr[1] = x_axis
        else:
            tmpArr = [float(tmpArr[i]) for i in range(len(tmpArr)) if i%2==0 or i==1]
        matrix.append(tmpArr[1:]) # after processing this row, add it to table
    f.close()
    from pandas import DataFrame
    df = DataFrame(matrix[1:], columns=matrix[0])
    return {"table1":df}, {"table1":{}}

def whichFileToLoad(fileName):
    possibilities = {
        ".dat": load_aixACCTFile,
        ".csv": load_probostatFile
    }
    for fileExtension in possibilities:
        if fileName.endswith(fileExtension):
            return possibilities[fileExtension](fileName)

# Test functions
def testFunction1():            
    allDataFramesFromTheFile = load_aixACCTFile("data/BSFO13_RS800_12h_10-150kVcm_RT.dat")
    print("\n\nHow many Data Frames were loaded: {}".format(len(allDataFramesFromTheFile)))

    for key in allDataFramesFromTheFile:
        tmp = allDataFramesFromTheFile[key]
        print("\n\n{} - size {}".format(key, tmp.shape))
        tmp.info()


import matplotlib.pyplot as plt
# Plot
def plotData(loadedTables, x_axis, y_axis):
    for file in loadedTables:
        # TODO if file checkboxed
        fileData = loadedTables[file]
        #print("+++++++++++++\n++++++++++++++++++\n\n\nDict {} key {}".format(loadedTables, file))
        #print(fileData)
        for contourName in fileData:
            # TODO if contour checkboxed
            contour =  fileData[contourName]
            #print("************************\n******************\n\n\nDict {} key {}".format(fileData, contourName))
            #print(contour)
            plt.plot(contour[x_axis], contour[y_axis])
        plt.show()
