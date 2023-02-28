import matplotlib.pyplot as plt
from improvedFunctions import load_aixACCTFile, load_probostatFile, whichFileToLoad, stitchUp_probostatFiles
import pandas as pd
import valueConversion
import os
import datetime
class brlopack:
    # self.data = dict[file][table][column]
    # self.wantedFiles = []
    # self.plotFiles {file:[True, False, True]}
    # self.constants[file][table] = [array of consatnts like area thickness etc]

    #@property
    def getConstants(self, unit = ""):
        retVal = {}
        for file in self.tellMeFiles():
            retVal[file] = {}
            for table in self.tellMeTablesInFile(file):
                retVal[file][table] = {}
                for const in self.constants[file][table]:
                    retVal[file][table][const] = self.getConstant(file, table, const, unit)
        return retVal
    
    def getConstant(self, file, table, const, unit = ""):
        try:
            if unit != "":
                return valueConversion.convertPrefix(self.constants[file][table][const], unit[0])
            else:
                return self.constants[file][table][const]
        except:
            return "NaN"

    def __init__(self, data=None):
        self.toPlot = []
        if data != None:
            self.data = data
            self.wantedFiles = (key for key in data)
        self.fig, self.ax = plt.subplots()
    
    # Tell files
    def browseDirectories(self):
        from tkinter import filedialog as fd 
        self.wantedFiles = fd.askopenfilenames()

    def tellFiles(self, files):
        self.wantedFiles = files

    # TODO input: path, extension, bool; outcome: load all files at the path, of the correct extension. if bool, load subdirs as well

    def loadFiles(self, optionalFunct = None):
        import time
        #time.sleep(1)
        if self.wantedFiles == None:
            raise Exception("IJS: I don't know which files to load. Either use `browseDirectories` function or the `tellFiles` function.")
        
        self.data = {}; self.plotFiles = {}; self.constants = {}

        try:
            if len(self.wantedFiles) > 1 and self.wantedFiles[0].endswith(".csv"): #TODO very ugly workaround
                self.data["Probostat"], self.constants["Probostat"] = stitchUp_probostatFiles(self.wantedFiles, "time [min]")
                self.wantedFiles = ["Probostat"]
            else:
                for file in self.wantedFiles:
                    self.data[file], self.constants[file] = whichFileToLoad(file, len(self.wantedFiles))
        except:
            for file in self.wantedFiles:
                self.data[file], self.constants[file] = whichFileToLoad(file, len(self.wantedFiles))
        
        
        for file in self.tellMeFiles():
            self.plotFiles[file] = {}
            for table in self.tellMeTablesInFile(file):
                #print("===========\n\n{file}   {table}")
                self.plotFiles[file][table] = True
                self.data[file][table].columns = self.data[file][table].columns.str.replace('°', '')
                self.data[file][table].columns = self.data[file][table].columns.str.replace('º', '')
        
        print("tell me what exception")

    # Inform of data 
    def tellMeFiles(self):
        return self.wantedFiles
    
    def tellMeTablesInFile(self, file):
        try:
            retVal = []
            for key in self.data[file]:
                retVal.append(key)
            return retVal
        except:
            raise Exception("IJS: No file named `{}` found here. Check for typos. Check if you called the `loadFiles` method.".format(file))
    
    def tellMeColumnsInTable(self, file, table):
        try:
            return [key for key in self.data[file][table]]
        except:
            raise Exception("IJS: No table named `{}` found in file `{}`. Check for typos.".format(table, file))

    def shouldIPlotFile(self, fileName, value):
        for table in self.plotFiles[fileName]:
            self.plotFiles[fileName][table] = value

    def shouldIPlotTables(self, fileName, table, truthValue):
        self.plotFiles[fileName][table] = truthValue
    
    def resetPlotSettings(self):
        for file in self.tellMeFiles():
            self.shouldIPlotFile(file, True)

    readyForPlotting = None
    def plotData(self, x_axis_columnName, y_axes_columnNames, fileName=None, tableNames=None, conditionColName=None, minimumValue=None, plotType="Line", show=True, showLegend=True, showGrid=False):    
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
            output_file_name = os.path.join(location, tmp +'_output.xlsx')
            with pd.ExcelWriter(output_file_name) as writer:  
                for table in self.tellMeTablesInFile(file):
                    if tablesToPlot != None:
                        if table not in tablesToPlot[file]: continue
                    self.data[file][table][columnNames].to_excel(writer, sheet_name=table)
            os.startfile(output_file_name)

    def doOperation(self, operation, columnName, newColumnName, constName):
        for file in self.tellMeFiles():
            for table in self.tellMeTablesInFile(file):
                if constName!=None:
                    try:
                        (constantVal, constantUnit) = self.constants[file][table][constName]
                    except:
                        continue
                else: constantVal = None
                arr = []
                for el in self.data[file][table][columnName]:
                    try: arr.append(operation(el, constantVal))
                    except: arr.append("NaN")

                self.data[file][table][newColumnName] = arr

    def divideConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el/const, columnName, newColumnName, constName)

    def multiplyConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el*const, columnName, newColumnName, constName)

    def subtractConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el-const, columnName, newColumnName, constName)

    def addConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el+const, columnName, newColumnName, constName)   

    def inverseColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**-1, columnName, newColumnName, constName)

    def squareColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**2, columnName, newColumnName, constName)
    
    def sqrtColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**0.5, columnName, newColumnName, constName)

    def averageTwoConstants(self, columnName, newColumnName, secondColumn):
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

    def changeUnitOfConstant(self, constantName, unitPrefix):
        for file in self.tellMeFiles():
            for table in self.tellMeTablesInFile(file):
                if constantName not in self.constants[file][table]: 
                    continue
                self.constants[file][table][constantName] = valueConversion.convertPrefix(self.constants[file][table][constantName], unitPrefix)

    def separateData(self, columnName):
        from splitting.newSplittingDF import forDataFrame
        for file in self.tellMeFiles():
            table = self.tellMeTablesInFile(file)[0]
            dataFrame = self.data[file][table]
            self.data[file], self.constants[file] = forDataFrame(dataFrame, columnName)
                
                
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