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

    # Separate column names
    columnNames = table[0]

    dataFrame = pd.DataFrame(
        data = np.array(table[1:]),
        columns=columnNames
        )

    if shouldPrint:
        print(dataFrame)

    return dataFrame

def getValue(string, valueName, terminator = "\n", suffix = ": ", subfunction = False):
    startIndex = string.index(valueName) +  len(valueName + suffix)
    terminatorIndex = string.index(terminator, startIndex) if terminator != None else len(string)

    numericData = string[startIndex : terminatorIndex]
    if subfunction:
        return numericData

    unitOfMeasurement = getValue(valueName, "[", terminator="]", suffix="", subfunction=True)

    return (numericData, unitOfMeasurement)

# Main function
def loadFile(fileName, printSummary = False):
    lines = fileToStr(fileName)

    sections = sectionTheFile(lines, printSummary)

    dataFrameList = {}
    for section in sections:
        tmpDataFrame = loadSection(section)
        dataFrameList[currentTableName] = tmpDataFrame
    
    return dataFrameList

# Test functions
def testFunction1():            
    allDataFramesFromTheFile = loadFile("data/BSFO13_RS800_12h_10-150kVcm_RT.dat")
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
