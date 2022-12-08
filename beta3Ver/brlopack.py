import matplotlib.pyplot as plt
from improvedFunctions import loadFile

class brlopack:
    # self.data = dict[file][table][column]
    # self.wantedFiles = []
    # self.plotFiles {file:[True, False, True]}

    def __init__(self, data=None):
        if data != None:
            self.data = data
    
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
        
        self.data = {}; self.plotFiles = {}
        for file in self.wantedFiles:
            self.data[file] = loadFile(file)
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
    """ 
    # Trim data
    def trimFiles(self, files):
        try:
            retVal = []
            for file in files:
                retVal.append(self.data[file])
            self.loadedTable = retVal
        except:
            raise Exception("IJS: Check spelling of files `{}`".format(files))

    def trimTablesInFile(self, file, tables):
        try:
            self.data[file] = [self.data[file][table] for table in tables]
        except:
            raise Exception("IJS: Check spelling of tables `{}` within the file `{}`".format(tables, file))
    
    def trimColumnsInTable(self, file, table, columns):
        try:
            self.data[file][table] = [self.data[file][table][column] for column in columns]
        except:
            raise Exception("IJS: Check spelling of columns `{}` within the table `{}` within the file `{}`".format(columns, table, file))
    
    # Looks like we didn't need trimming
    # questionable if we even need this
    def createView(self, fileTableDict, columns):
        # In order to preserve original data, we shall do the trimmings on a copy
        tmp = brlopack()
        tmp.tellFiles([file for file in fileTableDict])
        tmp.data = {}

        for file in fileTableDict:
            tmp.data[file] = {}
            tables = fileTableDict[file]
            if tables == None: tables = [table for table in self.data[file]]

            for table in tables:
                tmp.data[file][table] = self.data[file][table][columns]

        return tmp
    """
    def shouldIPlotFile(self, fileName, value):
        for table in self.plotFiles[fileName]:
            self.plotFiles[fileName][table] = value

    def shouldIPlotTables(self, fileName, table):
        self.plotFiles[fileName][table] ^= True
    

    def plotData(self, x_axis_columnName, y_axis_columnName, fileName=None):
        fig, ax = plt.subplots()

        files = self.tellMeFiles() if fileName == None else [fileName]

        for file in files:
            for table in self.tellMeTablesInFile(file):
                if not self.plotFiles[file][table]: continue
                x_data = self.data[file][table][x_axis_columnName]
                y_data = self.data[file][table][y_axis_columnName]
                plt.plot(x_data, y_data, label=table)
            plt.legend()
            plt.show()
    
"""    def readdDataToView(self, view, fileTableDict)"""
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