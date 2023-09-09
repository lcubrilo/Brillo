import matplotlib.pyplot as plt
from improvedFunctions import load_aixACCTFile, load_probostatFile, whichFileToLoad, stitchUp_probostatFiles
import pandas as pd
import valueConversion
import os
import datetime
from math import log, log1p

class brlopack:
    """
    Class with structure (file, table, column/constant)
    """
    # self.data = dict[file][table][column]
    # self.wantedFiles = []
    # self.plotFiles {file:[True, False, True]}
    # self.constants[file][table] = [array of consatnts like area thickness etc]

    #@property
    def getConstants(self, unit = ""):
        """
        Retrieves all constants from all loaded files and tables.

        Args:
            unit (str, optional): The unit to convert the constants to. Defaults to an empty string, meaning no conversion.

        Returns:
            dict: A nested dictionary containing all constants from all loaded files and tables.
        """
        retVal = {}
        for file in self.tellMeFiles():
            retVal[file] = {}
            for table in self.tellMeTablesInFile(file):
                retVal[file][table] = {}
                for const in self.constants[file][table]:
                    retVal[file][table][const] = self.getConstant(file, table, const, unit)
        return retVal
    
    def getConstant(self, file, table, const, unit = ""):
        """
        Retrieves a specific constant from a specified file and table.

        Args:
            file (str): The file name containing the table.
            table (str): The table name containing the constant.
            const (str): The name of the constant to retrieve.
            unit (str, optional): The unit to convert the constant to. Defaults to an empty string, meaning no conversion.

        Returns:
            float or str: The value of the specified constant, or "NaN" if not found.
        """
        try:
            if unit != "":
                return valueConversion.convertPrefix(self.constants[file][table][const], unit[0])
            else:
                return self.constants[file][table][const]
        except:
            return "NaN"
    
    def create_copy(self):
        import copy
        retVal = brlopack()
        retVal.constants = copy.deepcopy(self.constants)
        retVal.data = copy.deepcopy(self.data)
        retVal.plotFiles = copy.deepcopy(self.plotFiles)
        retVal.readyForPlotting = copy.deepcopy(self.readyForPlotting)
        retVal.toPlot = copy.deepcopy(self.toPlot)
        retVal.wantedFiles = copy.deepcopy(self.wantedFiles)
        return retVal
        

    def __init__(self, data=None):
        """
        Initializes the brlopack object with optional data.

        Args:
            data (dict, optional): The initial data to populate the object. Defaults to None.
        """
        self.toPlot = [] #TODO obrisati?
        if data != None:
            self.data = data
            self.wantedFiles = (key for key in data)
        
    
    # Tell files
    def browseDirectories(self):
        """
        Creates a GUI popup for the user to select a directory from which to load the files and tables.
        """
        from tkinter import filedialog as fd 
        self.wantedFiles = fd.askopenfilenames()

    def tellFiles(self, files):
        """
        Manual selection of loaded files through a parameter instead of the GUI.
        Setter for field wantedFiles (should initiate loading data)

        Args:
            files (list of str): The list of file paths to load.
        """
        self.wantedFiles = files

    # TODO input: path, extension, bool; outcome: load all files at the path, of the correct extension. if bool, load subdirs as well

    def loadFiles(self, optionalFunct = None):
        """
        Based on the wantedFiles field, loads the data (tables/columns) and constants. 
        Initializes "should plot" to True for all tables.

        Args:
            optionalFunct (callable, optional): An optional function to apply during loading (such as a progressbar or smth). Defaults to None.

        Raises:
            Exception: If no files are specified to load.
        """

        import time, os.path
        #time.sleep(1)
        if self.wantedFiles == None:
            raise Exception("IJS: I don't know which files to load. Either use `browseDirectories` function or the `tellFiles` function.")
        doesntExist = []
        notafile = []
        for file in self.wantedFiles:
            if not os.path.exists(file):
                doesntExist.append(file)
            if not os.path.isfile(file):
                notafile.append(file)
        if doesntExist != [] or notafile != []:
            raise Exception(f"IJS: The following paths do not exist: {doesntExist}, and these are not files: {notafile}")

        self.data = {}; self.plotFiles = {}; self.constants = {}

        try:
            if len(self.wantedFiles) > 1 and self.wantedFiles[0].endswith(".csv"): #TODO very ugly workaround
                print("Will load probostat files")
                self.data["Probostat"], self.constants["Probostat"] = stitchUp_probostatFiles(self.wantedFiles, "time [min]")
                self.wantedFiles = ["Probostat"]
            else:
                print("Will not load probostat files")
                for file in self.wantedFiles:
                    self.data[file], self.constants[file] = whichFileToLoad(file, len(self.wantedFiles))
        except Exception as e:
            print("Exception found during file loading, trying alternative")
            print(f"Exception: {e}")
            for file in self.wantedFiles:
                self.data[file], self.constants[file] = whichFileToLoad(file, len(self.wantedFiles))
        
        
        for file in self.tellMeFiles():
            self.plotFiles[file] = {}
            for table in self.tellMeTablesInFile(file):
                #print("===========\n\n{file}   {table}")
                self.plotFiles[file][table] = True
                self.data[file][table].columns = self.data[file][table].columns.str.replace('°', '')
                self.data[file][table].columns = self.data[file][table].columns.str.replace('º', '')
        
        #print("tell me what exception")

    # Inform of data 
    def tellMeFiles(self):
        """
        Getter for field wantedFiles

        Returns:
        list: A list of loaded file names.
        """
        return self.wantedFiles
    
    def tellMeTablesInFile(self, file):
        """
        Getter for list of tables, given a file.

        Args:
        file (str): The file name containing the tables.

        Returns:
            list: A list of table names in the specified file.

        Raises:
            Exception: If the specified file is not found.
        """
        try:
            retVal = []
            for key in self.data[file]:
                retVal.append(key)
            return retVal
        except:
            raise Exception("IJS: No file named `{}` found here. Check for typos. Check if you called the `loadFiles` method.".format(file))
    
    def tellMeColumnsInTable(self, file, table):
        """
        Getter for list of columns, given a file AND table.
        Note: still not determined if all tables of a file should have the same columns; up to debate.
            Even less clear if that should apply for all files in a session.
        
        Args:
            file (str): The file name containing the table.
            table (str): The table name containing the columns.

        Returns:
            list: A list of column names in the specified table within the specified file.

        Raises:
            Exception: If the specified table is not found in the specified file.
        """
        try:
            return [key for key in self.data[file][table]]
        except:
            raise Exception("IJS: No table named `{}` found in file `{}`. Check for typos.".format(table, file))

    def shouldIPlotFile(self, fileName, value):
        """
        Setter for plotFiles field. Applies same value to all tables of a file.
        Triggers when checking and unchecking checkbox of a file in left part of the GUI.

        Args:
            fileName (str): The name of the file to update the plotting status for.
            value (bool): The plotting status to set for all tables in the specified file.
        """
        for table in self.plotFiles[fileName]:
            self.plotFiles[fileName][table] = value

    def shouldIPlotTables(self, fileName, table, truthValue):
        """
        Setter for plotFiles field. Applies to only one table of a file.
        Triggers when checking and unchecking checkbox of a table int left part of the GUI.
        """
        self.plotFiles[fileName][table] = truthValue
    
    def resetPlotSettings(self):
        """
        Set the value of plotFiles for all files and tables back to the default (True)
        
        Note: Not sure if it is ever triggered by GUI in current version. Maybe when refreshing?
        """
        for file in self.tellMeFiles():
            self.shouldIPlotFile(file, True)

    readyForPlotting = None
    def plotData(self, x_axis_columnName, y_axes_columnNames, fileName=None, tableNames=None, conditionColName=None, minimumValue=None, plotType="Line", show=True, showLegend=True, showGrid=False):    
        """
        Plots data of multiple y axes given a common x axis. (Note: Implemented through subplots, but overlapping also possible!!!)    
        
        Can perform on a subset of selected files/tables.
        Can be with or without legend and grid.
        Further customization possible through arguments.

        Args:
            x_axis_columnName (str): The column name for the x-axis.
            y_axes_columnNames (list): A list of column names for the y-axes.
            fileName (str or list, optional): The name(s) of the file(s) to plot. Defaults to None, meaning all files.
            tableNames (dictionary, optional): fileName is key, while a list of table names to plot is value. Defaults to None, meaning all tables.
            conditionColName (str, optional): Not used in the current implementation.
            minimumValue (float, optional): Not used in the current implementation.
            plotType (str, optional): Type of plot ("Line", "Dotted", "Both"). Defaults to "Line".
            show (bool, optional): Whether to display the plot. Defaults to True. 
            showLegend (bool, optional): Whether to display the legend. Defaults to True.
            showGrid (bool, optional): Whether to display the grid. Defaults to False.
        """
        
        n = len(y_axes_columnNames)
        self.fig, self.axs = plt.subplots(n)
        x_min = 1.7976931348623157e+308 
        x_max = -1.7976931348623157e+308
        if n == 0: return
        if n == 1: self.axs = [self.axs]
        
        if fileName == None:
            files = self.tellMeFiles()
        elif type(fileName) == list:
            files = fileName
        elif type(fileName) == set:
            files = list(fileName)
        else:
            files = [fileName]

        for i, y_axis_columnName in enumerate(y_axes_columnNames):
            for file in files:
                for table in self.tellMeTablesInFile(file):
                    if tableNames == None:
                        if not self.plotFiles[file][table]:
                            continue
                    else:
                        if table not in tableNames[file]:
                            continue
                        
                    x_data = self.data[file][table][x_axis_columnName]
                    y_data = self.data[file][table][y_axis_columnName]
                    self.axs[i].set_xlabel(x_axis_columnName)
                    self.axs[i].set_ylabel(y_axis_columnName)
                    label = table+"_"+y_axis_columnName if showLegend else ""
                    

                    if plotType == "Line":
                        self.axs[i].plot(x_data, y_data, label=label)
                    elif plotType == "Dotted":
                        self.axs[i].scatter(x_data, y_data, label=label)
                    elif plotType == "Both":
                        self.axs[i].plot(x_data, y_data, label=label)
                        self.axs[i].scatter(x_data, y_data, label=label)
                    else:
                        raise Exception("IJS: Plot doesn't know whether to be line or dotted")

                    tmp_min, tmp_max = self.axs[i].get_xlim()
                    if tmp_min < x_min: x_min = tmp_min
                    if tmp_max > x_max: x_max = tmp_max

                if showGrid:
                    self.axs[i].grid()
                
                if showLegend:
                    self.axs[i].legend()

        for i, y_axis_columnName in enumerate(y_axes_columnNames):
            self.axs[i].set_xlim(x_min, x_max)

        plt.show()
        

    def exportToExcel(self, location=None, columnNames=None, filesToPlot = None, tablesToPlot = None):
        """
        Exports all data of the session into an Excel xlsx file to a given filepath (or by default to the location where data was loaded from)
        
        You can exclude uninteresting files, tables, even columns (same like with the plotting)
        Exported filename format is "Brillo export [date time].xlsx" by default.

        Args:
            location (str, optional): The file path to export to. Defaults to the location where data was loaded from.
            columnNames (list, optional): A list of column names to export. Defaults to all columns.
            filesToPlot (list, optional): A list of file names to export. Defaults to all files.
            tablesToPlot (list, optional): A list of table names to export. Defaults to all tables.
        """
        if location == None or location == False:
            location = os.path.dirname(self.tellMeFiles()[0])
        now = datetime.datetime.now()
        now_str = "Brillo export " + now.strftime("%Y-%b-%d; ") + now.strftime("%H-%M-%S")

        location = os.path.join(location, now_str)
        if not os.path.exists(location):
            os.makedirs(location)
        
        if columnNames == None:
            firstFile = self.tellMeFiles()[0]
            firstTable = self.tellMeTablesInFile(firstFile)[0]
            columnNames = self.tellMeColumnsInTable(firstFile, firstTable)
        
        if filesToPlot == None: filesToPlot = self.tellMeFiles()
        #if tablesToPlot == None: tablesToPlot = self.tellMeTablesInFile(filesToPlot[0])

        for file in filesToPlot:
            tmp = os.path.basename(file)
            output_file_name = os.path.join(location, tmp +'_output.xlsx') #TODO make it an arg
            with pd.ExcelWriter(output_file_name) as writer:  
                for table in self.tellMeTablesInFile(file):
                    if tablesToPlot != None:
                        if table not in tablesToPlot[file]: continue
                    self.data[file][table][columnNames].to_excel(writer, sheet_name=table)
            try:
                os.startfile(output_file_name)
            except Exception as e:
                print("Couldn't open the outputted Excel file: ", e)

    def doOperation(self, operation, columnName, newColumnName, constName):
        """
        Performs a given operation/function from one input column to a newly created output column.
        Can also use 1 constant from its table (depending on if the operation needs it or uses it; and if it is found)
        
        Args:
            operation (function): The function to apply to the column.
            columnName (str): The name of the input column.
            newColumnName (str): The name of the output column.
            constName (str, optional): The name of a constant to use in the operation. Defaults to None.
        """
        for file in self.tellMeFiles():
            for table in self.tellMeTablesInFile(file):
                if constName!=None:
                    try:
                        (constantVal, constantUnit) = self.constants[file][table][constName]
                    except:
                        continue #TODO: is the behaviour of constVal defined here??
                else: constantVal = None
                arr = []
                for el in self.data[file][table][columnName]:
                    try: arr.append(operation(el, constantVal))
                    except: arr.append("NaN") #TODO: I think this is the answer to the previous question

                self.data[file][table][newColumnName] = arr

    def logN(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:log1p(el), columnName, newColumnName, constName)

    def logConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:log(el, const), columnName, newColumnName, constName)
    #TODO logs dont do anything
    def divideConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el/const, columnName, newColumnName, constName)

    def multiplyConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el*const, columnName, newColumnName, constName)

    def subtractConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el-const, columnName, newColumnName, constName)

    def addConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el+const, columnName, newColumnName, constName)   

    def inverseColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**-1, columnName, newColumnName, constName)

    def squareColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**2, columnName, newColumnName, constName)
    
    def sqrtColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**0.5, columnName, newColumnName, constName)

    def averageTwoColumns(self, columnName, newColumnName, secondColumn):
        """
        Takes two columns, creates new column as their average.
        Works over all files and all tables.

        Args:   
            columnName (str): The name of the first input column.
            newColumnName (str): The name of the output column.
            secondColumn (str): The name of the second input column.
        """
        for file in self.tellMeFiles():
            for table in self.tellMeTablesInFile(file):
                tmpArr = []
                tableData = self.data[file][table]

                col1 = tableData[columnName]
                col2 = tableData[secondColumn]

                for el1, el2 in zip(col1, col2):
                    try:
                        tmpArr.append((el1+el2)/2)
                    except:
                        tmpArr.append("NaN")

                tableData[newColumnName] = tmpArr

    def changeUnitOfColumn(self, columnName, newColumnName):
        from arrayConversion import adapter_ConvertPrefix
        adapter_ConvertPrefix(self, columnName, newColumnName)

    def changeUnitOfConstant(self, constantName, unitPrefix):
        """
        Looks for all occurences of constant in all files and tables.
        Sets all occurences to the same unit.
        Note: still not agreed if all file/tables should have the same set of constants!

        Args:
            constantName (str): The name of the constant to change the unit.
            unitPrefix (str): The new unit prefix to apply to the constant.
        """
        for file in self.tellMeFiles():
            for table in self.tellMeTablesInFile(file):
                if constantName not in self.constants[file][table]: 
                    continue
                self.constants[file][table][constantName] = valueConversion.convertPrefix(self.constants[file][table][constantName], unitPrefix)

    def separateData(self, columnName):
        """
        BIG NOTE: Assumes data follows the pattern of ____/¯¯¯¯¯¯¯\_ (low, rise, high, drop) due to many bugs for a generalized version.
        BIG NOTE 2: If generalized version is needed, let me know, it will take some time.
        Separating data into rise, flat and drop.
        Used for Probostat data.
        Note: Untested/undefined behaviour for multiple files or table. Usually used after stitching multiple files into one and only file.
    
        Args:
            columnName (str): The name of the column used for the separation criteria.
        """
        from splitting.newSplittingDF import forDataFrame
        for file in self.tellMeFiles():
            table = self.tellMeTablesInFile(file)[0] # assumes only one table in the file needs to be split
            dataFrame = self.data[file][table]
            self.data[file], self.constants[file], self.plotFiles[file] = forDataFrame(dataFrame, columnName)
                
# tests
def testLoad():
    paket = brlopack()
    paket.browseDirectories()
    paket.loadFiles()
    return paket

def playingAround(paket):
    print("\nKoje fajlove imamo?")
    fajlovi = paket.tellMeFiles(); prviFajl = fajlovi[0]
    for file in fajlovi:
        print("\t", file)

    print("\n Koje tabele imamo u prvom fajlu?")
    tabele = paket.tellMeTablesInFile(prviFajl); prvaTabela = tabele[0]
    for table in tabele:
        print("\t", table)

    print("\n Koje kolone imamo u prvoj tabeli u prvom fajlu?")
    kolone = paket.tellMeColumnsInTable(prviFajl, prvaTabela)
    for column in kolone:
        print("\t", column)
        #print("\n\n", paket.loadedTables[prviFajl][prvaTabela][column])

def creatingSubview(paket):
    myDict1 = {
        "C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS800_12h_10-150kVcm_RT.dat":None,
        "C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS820_10-150kVcm_RT.dat":None
        }

    subsetOfColumns = [
        "V+ [V]",
        "V- [V]",
        "I1 [A]",
        "P1 [uC/cm2]",
        "I2 [A]",
        "P2 [uC/cm2]"
    ]

    paket2 = paket.createView(myDict1, subsetOfColumns)
    print("\n\n\n\n\////////////////////VIEW////////////////////\n")
    playingAround(paket2)

if __name__ == "__main__":
    playingAround(testLoad())