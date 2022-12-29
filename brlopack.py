import matplotlib.pyplot as plt
from improvedFunctions import load_aixACCTFile, load_probostatFile, whichFileToLoad
import pandas as pd
import valueConversion
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
        if data != None:
            self.data = data
            self.wantedFiles = (key for key in data)
    
    # Tell files
    def browseDirectories(self):
        from tkinter import filedialog as fd 
        self.wantedFiles = fd.askopenfilenames()

    def tellFiles(self, files):
        self.wantedFiles = files

    # TODO input: path, extension, bool; outcome: load all files at the path, of the correct extension. if bool, load subdirs as well

    def loadFiles(self):
        if self.wantedFiles == None:
            raise Exception("IJS: I don't know which files to load. Either use `browseDirectories` function or the `tellFiles` function.")
        
        self.data = {}; self.plotFiles = {}; self.constants = {}
        for file in self.wantedFiles:
            self.data[file], self.constants[file] = whichFileToLoad(file)
            self.plotFiles[file] = {}
            for table in self.data[file]:
                self.plotFiles[file][table] = True

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

    def plotData(self, x_axis_columnName, y_axis_columnName, fileName=None, tableNames=None):
        fig, ax = plt.subplots()

        if fileName == None:
            files = self.tellMeFiles()
        elif type(fileName) == list:
            files = fileName
        elif type(fileName) == set:
            files = list(fileName)
        else:
            files = [fileName]

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
                plt.xlabel(x_axis_columnName)
                plt.ylabel(y_axis_columnName)
                plt.plot(x_data, y_data, label=table)
            plt.legend()
        plt.show()
    
    def exportToExcel(self):
        for file in self.tellMeFiles():
            with pd.ExcelWriter(file+'_output.xlsx') as writer:  
                for table in self.tellMeTablesInFile(file):
                    self.data[file][table].to_excel(writer, sheet_name=table)

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

    def divideConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el*const, columnName, newColumnName, constName)

    def subtractConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el-const, columnName, newColumnName, constName)

    def addConstant(self, columnName, newColumnName, constName): self.doOperation(lambda el, const:el+const, columnName, newColumnName, constName)   

    def inverseColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**-1, columnName, newColumnName, constName)

    def squareColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**2, columnName, newColumnName, constName)
    
    def sqrtColumn(self, columnName, newColumnName, constName=None): self.doOperation(lambda el, const:el**0.5, columnName, newColumnName, constName)


    def changeUnitOfConstant(self, constantName, unitPrefix):
        for file in self.tellMeFiles():
            for table in self.tellMeTablesInFile(file):
                if constantName not in self.constants[file][table]: 
                    continue
                self.constants[file][table][constantName] = valueConversion.convertPrefix(self.constants[file][table][constantName], unitPrefix)
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