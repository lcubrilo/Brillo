import pandas as pd
import numpy as np
from splitting.newSplittingDF import forDataFrame

##############################################
#region ########### a i x A C C T ############
# Helper functions
def fileToStr(fileName):
    """
    Reads the contents of a file and returns them as a single string.

    Args:
        fileName (str): Path to the file to be read.

    Returns:
        str: Contents of the file as a single string.
    """
    print("Loading file {}".format(fileName))
    lines = ""
    with open(fileName) as f:
        for line in f:
            lines += line

    return lines

def sectionTheFile(lines, printSummary):
    """
    For aixACCT - sections off the file content into separate tables.

    Args:
        lines (str): The entire content of the file as a single string.
        printSummary (bool): Flag to indicate whether to print the summary or not.

    Returns:
        list: List of sections (tables) from the file, excluding the summary.
    """
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
    """
    For aixACCT - Loads each section of the aixACCT file into separate tables, including preprocessing.

    Args:
        section (str): A string representing a section of the file containing a table.
        shouldPrint (bool, optional): Flag to print the data frame. Defaults to False.
        sectionName (str, optional): Name for the section. Defaults to "Contour ".

    Returns:
        tuple: DataFrame representing the table, and interesting constants (e.g., area, thickness).
    """
    # Some preprocessing
    lastLine = "Measurement Status:"
    index = section.index("\n",section.index(lastLine))+1
    
    dataBeforeTable = section[:index]
    
    global currentTableName; redniBrojTabele = dataBeforeTable[:dataBeforeTable.index("\n")]
    
    # AFAIK the only useful data we need are area and thickness. TODO check if we need others
    area = getValue(dataBeforeTable, "Area [mm2]")
    thickness = getValue(dataBeforeTable, "Thickness [nm]") # TODO doesn't get unit of measurement SADA GA DOBIJA, ZASTO
    try:
        amplitude = getValue(dataBeforeTable, "Hysteresis Amplitude [V]")

        thickness_val_cm = thickness[0]/10e7
        amp_val_kv = amplitude[0]/10e3
        el_field_strength = round(amp_val_kv/thickness_val_cm, 6)

        currentTableName = "{}.  {} kV_cm".format(redniBrojTabele, el_field_strength)
    except:
        currentTableName = sectionName + redniBrojTabele

    #thickness = float(thickness[0]) # That perhaps answers the question above. Why do this?

    # Now get the table from the string - MAIN PART
    table = section.strip()[index:].split("\n")
    if table[-1] == "Data": table = table[:-1]
    for i, line in enumerate(table):
        table[i] = table[i].strip().split("\t")
        if i == 0: continue
        if table[i] == "" or len(table[i]) == 1 or type(table[i]) != type(list()): table.remove(table[i]); continue
        
        for j, cell in enumerate(table[i]):
            try:
                table[i][j] = float(table[i][j])
            except:
                continue

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
    """
    For aixACCT - Reads specific constants or values from a section of an aixACCT table given its value name.

    Args:
        string (str): The portion of the section containing the value to be read.
        valueName (str): Name of the value or constant to be retrieved.
        terminator (str, optional): Character indicating the end of the value. Defaults to "\n".
        suffix (str, optional): String that comes after the value name. Defaults to ": ".
        subfunction (bool, optional): Flag to indicate use as a subfunction. Defaults to False.

    Returns:
        tuple or str: Numeric value and unit, or raw numeric data as a string if subfunction is True.
    """
    startIndex = string.index(valueName) +  len(valueName + suffix)
    terminatorIndex = string.index(terminator, startIndex) if terminator != None else len(string)

    numericData = string[startIndex : terminatorIndex]
    if subfunction:
        return numericData

    unitOfMeasurement = getValue(valueName, "[", terminator="]", suffix="", subfunction=True)

    return (float(numericData), unitOfMeasurement)

# Main function
def load_aixACCTFile(fileName, printSummary = False):
    """
    For aixACCT - Orchestrates the reading of an entire aixACCT file, including sectioning and loading tables.

    Args:
        fileName (str): Path to the .dat aixACCT file to be read.
        printSummary (bool, optional): Flag to indicate whether to print the summary. Defaults to False.

    Returns:
        tuple: Dictionary of DataFrames representing the tables, and a dictionary of associated constants.

    Raises:
        Exception: If the provided file does not have the .dat extension.
    """
    if not fileName.endswith(".dat"): raise Exception("Expected a .dat file of aixACCT.")
    lines = fileToStr(fileName)

    sections = sectionTheFile(lines, printSummary)

    dataFrameDict = {}; constantsDict ={}
    for section in sections:
        tmpDataFrame, constants = loadSection(section)
        dataFrameDict[currentTableName] = tmpDataFrame
        constantsDict[currentTableName] = constants
    
    return dataFrameDict, constantsDict
#endregion

##################################################
#region ########### P R O B O S T A T ############

def load_probostatFile(fileName, subFunction=False):
    """
    Reads and organizes data from a Probostat .csv file into a DataFrame.
    Called within 'stitchUp_probostatFiles' as a subfunction when multiple files are provided.

    Args:
        fileName (str): Path to the .csv Probostat file to be read.
        subFunction (bool, optional): Flag to indicate use as a subfunction. Defaults to False.

    Returns:
        tuple: Dictionary containing the DataFrame, and a dictionary for constants.

    Raises:
        Exception: If the provided file does not have the .csv extension.
    """
    if not fileName.endswith(".csv"): raise Exception("Expected a .csv file of Probostat.")
    f = open(fileName, "r") # open the file
    matrix = [] # get an empty table ready
    x_axis = None
    i = 0
    for line in f: # go line by line in file - that is gonna become our rows in table
        # Get x axis from pre-table data
        if not x_axis and line.startswith(";Assigned to Axis: "):
            index = line.find(";Assigned to Axis: ") + len(";Assigned to Axis: ")
            x_axis = line[index:].strip()

        # skip empty rows; "\n" means "newline"
        if line == "\n":
            continue 
        
        tmpArr = line.split(";") # separate values by the ";" character and store in a temporary array
        
        # they always had the first one empty, delete it
        if len(tmpArr) > 1:
            tmpArr=tmpArr[1:] 
        
        # if it has just one element it is pre-table bullshit
        if len(tmpArr) == 1:
            continue 

        #if line.count("NAN") > len(tmpArr)-1 or line.count("nan") > len(tmpArr)-1:#if line.__contains__("NAN") or line.__contains__("nan"):
        #if line.count("NAN") > 0 or line.count("nan") > 0:
            #break#break
        
        if not tmpArr[0].isdigit(): # this only happens in the header row (where names of columns are)
            n = len("X data for ")
            for i in range(1, len(tmpArr)):
                tmpArr[i] = tmpArr[i][n:] # this removes "X data for " from beginning of column name
            tmpArr = [tmpArr[i] for i in range(len(tmpArr)) if i%2==0 or i==1]
            tmpArr[1] = x_axis
        else:
            i+=1
            tmpArr = [float(tmpArr[i]) for i in range(len(tmpArr)) if i%2==0 or i==1]
            if i > 4060:
                print("yo")
        # after processing this row, add it to table
        matrix.append(tmpArr) #removes index column
        #matrix.append(tmpArr) #keeps index column
    f.close()
    
    df = pd.DataFrame(matrix, columns=matrix[0])
    #return {"table1":df}, {"table1":{}}
    
    #df = df.dropna()
    if not subFunction:
        dictionary = forDataFrame(df, "AVG T  [°C]")
        print("all good")
        constants = {key:{} for key in dictionary}
        return dictionary, constants
    else:
        return df

x_axis= None
def load_probostatFile_stitching(fileName, subFunction=False):
    """
    Processes a Probostat .csv file, extracting and organizing the data into a DataFrame.
    Used as a subfunction within 'stitchUp_probostatFiles' for stitching multiple files.

    Args:
        fileName (str): Path to the .csv Probostat file to be read.
        subFunction (bool, optional): Flag to indicate use as a subfunction. Defaults to False.

    Returns:
        DataFrame: Resulting DataFrame containing data extracted from the file.

    Raises:
        Exception: If the provided file does not have the .csv extension or if the file is not valid.
    """
    if not fileName.endswith(".csv"): raise Exception("Expected a .csv file of Probostat.")
    f = open(fileName, "r") # open the file
    matrix = [] # get an empty table ready
    global x_axis
    x_axis = None

    n = None
    columnNames = []; dataFrames = []
    setOfTimes = set()
    for j, line in enumerate(f): # go line by line in file - that is gonna become our rows in table
        # Get x axis from pre-table data
        if not x_axis and line.startswith(";Assigned to Axis: "):
            index = line.find(";Assigned to Axis: ") + len(";Assigned to Axis: ")
            x_axis = line[index:].strip()

        # skip empty rows; "\n" means "newline"
        if line == "\n":
            continue 
        
        tmpArr = line.split(";") # separate values by the ";" character and store in a temporary array
        
        # they always had the first one empty, delete it
        if len(tmpArr) > 1:
            tmpArr=tmpArr[1:] 
        
        # if it has just one element it is pre-table bullshit
        if len(tmpArr) == 1:
            continue 

        tmpArr = tmpArr[1:]
        if tmpArr[-1] == "\n":
            tmpArr = tmpArr[:-1]

        try:
            float(tmpArr[0])
            isHeader = False
        except:
            isHeader = True

        if isHeader: # this only happens in the header row (where names of columns are)
            if columnNames != []:
                raise Exception("Not expected order of operations")
            
            n = len(tmpArr)
            nn = len("X data for ")
            for i in range(0, n):
                tmpArr[i] = tmpArr[i][nn:] # this removes "Y data for " from beginning of column name
                if i == 0:
                    columnNames.append(x_axis)
                if i%2==1:
                    columnNames.append(tmpArr[i])
                    dataFrames.append(pd.DataFrame(columns=[x_axis, columnNames[-1]]))

            continue

        if n != len(tmpArr):
            raise Exception("CSV file is not valid")

        for i in range(len(tmpArr)):
            if i%2 == 1: continue
            x = tmpArr[i]
            y = tmpArr[i+1]
            if x == "NAN" or y=="NAN":continue
            x = round(float(x), 6)
            y = round(float(y), 6)
            yColName = columnNames[1+ i//2]
            setOfTimes.add(x)
            newRow = pd.Series({x_axis:x,yColName:y})
            dataFrames[i//2] = pd.concat([dataFrames[i//2], newRow.to_frame().T],ignore_index=True)

        
    f.close()

    #matrix is whole table together
    #first row colnames, all others table
    listOfTimes = sorted(list(setOfTimes))
    result = pd.DataFrame({x_axis:listOfTimes})

    for df in dataFrames:
        newResult = pd.merge(result, df, on=x_axis, how='outer')
        result = newResult
    #df = pd.concat(dataFrames, axis=0, ignore_index=True)
    #return {"table1":df}, {"table1":{}}
    
    #df = df.dropna()
    """if not subFunction:
        dictionary = forDataFrame(result, "AVG T  [°C]")
        print("all good")
        constants = {key:{} for key in dictionary}
        return dictionary, constants
    else:"""
    #return {"table":result}, {"table":{}}
    return result

if __name__ == "__main__":
    #testSplitRiseFlatFall()
    rollings = [1, 5, 50, 150]
    epsilons = [10**-6, 10**-4, 10**-2, 0.02, 0.05, 0.1, 1, 2, 5]

    for roll in rollings:
        for eps in epsilons:
            rolling = roll; epsilon = eps
            testForDataFrame()

#endregion

######################################
#region ########### MISC ############

def load_excel(fileName):
    """
    Loads data from an Excel file into a DataFrame.

    Args:
        fileName (str): Path to the Excel file to be read.

    Returns:
        tuple: Dictionary of DataFrames (one for each sheet), and an empty dictionary for constants.
    """
    dataFrames = {}; constants = {}
    for sheetName in pd.ExcelFile(fileName).sheet_names:
        dataFrames[sheetName] = pd.read_excel(fileName, sheet_name=sheetName)
        constants[sheetName] = dict()

    return dataFrames, constants

def load_csv(fileName):
    """
    Loads data from a .csv file into a DataFrame using the appropriate delimiter.

    Args:
        fileName (str): Path to the .csv file to be read.

    Returns:
        tuple: Dictionary containing the DataFrame, and an empty dictionary for constants.
    """
    # First remove all instances of 0xb0 character (degree)
    import csv

    with open(fileName, 'r') as infile:
        rows = [[cell.replace('\xb0', '') for cell in row] for row in csv.reader(infile)]

    with open(fileName, 'w', newline='') as outfile:
        csv.writer(outfile).writerows(rows)

    #find separator
    import subprocess

    result = subprocess.run(['csvstat', fileName], stdout=subprocess.PIPE)
    output = result.stdout.decode()

    try:
        delimiter = output.split('Delimiter: ')[1].split('\n')[0]

        return {"csv table":pd.read_csv(fileName, sep=delimiter)}, {"csv table":dict()}
    except:
        return {"csv table":pd.read_csv(fileName)}, {"csv table":dict()}

def whichFileToLoad(fileName, n):
    """
    Determines the appropriate loading function based on the file extension.

    Args:
        fileName (str): Path to the file to be read.
        n (int): An additional parameter (unused in the current implementation).

    Returns:
        function: The corresponding loading function for the given file extension.
    """
    possibilities = {
        ".dat": load_aixACCTFile,
        ".csv": load_csv,
        ".xlsx": load_excel
    }

    for fileExtension in possibilities:
        if fileName.endswith(fileExtension):
            return possibilities[fileExtension](fileName)



import matplotlib.pyplot as plt
# Plot
def plotData(loadedTables, x_axis, y_axis, conditionColName=None, minimumValue=None, plotType="Line"):
    """
    Plots data from a DataFrame using specified columns for the x and y axes.
    
    Args:
        dataFrame (DataFrame): DataFrame containing the data to be plotted.
        xColumn (str): Name of the column to be used for the x-axis.
        yColumns (list): List of column names to be used for the y-axis.
        title (str): Title of the plot.
        xLabel (str): Label for the x-axis.
        yLabel (str): Label for the y-axis.
        legendLabels (list): List of labels for the legend corresponding to yColumns.
        saveName (str): Path and filename to save the plot as an image file.

    Returns:
        None: The function displays the plot and saves it to the specified location.
    """
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
            #df = contour.dropna() TODO
            if conditionColName != None and minimumValue != None:
                df.drop(df[df[conditionColName] < minimumValue].index, inplace=True)
            if plotType == "Line":
                plt.plot(df[x_axis], df[y_axis])
            elif plotType == "Dotted":
                plt.scatter(df[x_axis], df[y_axis])
            else:
                raise Exception("Plot doesn't know whether to be line or dotted")
        plt.show()

#endregion

def stitchUp_probostatFiles(fileList, separationColumn):
    """
    Stitches together multiple Probostat files into a single DataFrame by aligning common columns
    and appending unique data. Useful for consolidating different measurements or conditions.

    Args:
        fileList (list): List of file paths for the Probostat files to be stitched together.
        separationColumn (str): Name of the column used for separation and alignment (e.g., time).

    Returns:
        tuple: Dictionary containing the resulting DataFrame, and a dictionary for constants.
    """
    loadedDataFrames = []
    for file in fileList:
        loadedDataFrames.append(load_probostatFile_stitching(file, True))
    
    #df = pd.concat(loadedDataFrames, axis=0, ignore_index=True)

    global x_axis
    result = pd.DataFrame({x_axis:[]})
    for df in loadedDataFrames:
        newResult = pd.merge(result, df, on=x_axis, how='outer')
        result = newResult

    """dictionary = forDataFrame(result, separationColumn)
    print("all good")
    constants = {key:{} for key in dictionary}
    return dictionary, constants"""
    result = result.sort_values(by=[x_axis])
    return {"table":result}, {"table":{}}

# Test functions
def testFunction1():            
    allDataFramesFromTheFile = load_aixACCTFile("data/BSFO13_RS800_12h_10-150kVcm_RT.dat")
    print("\n\nHow many Data Frames were loaded: {}".format(len(allDataFramesFromTheFile)))

    for key in allDataFramesFromTheFile:
        tmp = allDataFramesFromTheFile[key]
        print("\n\n{} - size {}".format(key, tmp.shape))
        tmp.info()