try:
    from brlopack import brlopack
    print("Successfully loaded `brlopack` from `brlopack`")
except:
    print("!!!!!!!!!!!!!")
    print("ERROR: Importing the package was NOT successful.")


paket = brlopack()
paket.browseDirectories()

paket.loadFiles()



paket.tellMeFiles()


paket.tellMeTablesInFile("C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS800_10-150kVcm_RT.dat")




some_uniquely_defined_table = paket.data["C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS800_10-150kVcm_RT.dat"]["Contour 1"]
some_uniquely_defined_table


some_uniquely_defined_table.info()


some_uniquely_defined_table["P1 [uC/cm2]"]


time = some_uniquely_defined_table["Time [s]"]
voltage = some_uniquely_defined_table["V+ [V]"]
p1 = some_uniquely_defined_table["P1 [uC/cm2]"]
john = some_uniquely_defined_table["P2 [uC/cm2]"]

john 



voltage





for file in paket.tellMeFiles():
    for table in paket.tellMeTablesInFile(file):
        print(paket.constants[file][table])


from valueConversion import convertPrefix
def changeUnitOfConstant(package, constantName, unitPrefix):
    for file in package.tellMeFiles():
        for table in package.tellMeTablesInFile(file):
            package.constants[file][table][constantName] = convertPrefix(package.constants[file][table][constantName], unitPrefix)
    
changeUnitOfConstant(paket, "thickness", "c")


def divide(package, columnName, newColumnName, constName):
    for file in paket.tellMeFiles():
        for table in paket.tellMeTablesInFile(file):
            (constantVal, constantUnit) = paket.constants[file][table][constName]
            paket.data[file][table][newColumnName] = [el/constantVal for el in paket.data[file][table][columnName]]

divide(paket, "V+ [V]", "E+ [V/cm]", "thickness") 
divide(paket, "V- [V]", "E- [V/cm]", "thickness") 


divide(paket, "D3 [nm]", "delta3 [%]", "thickness")
divide(paket, "D2 [nm]", "delta2 [%]", "thickness")


for el in paket.data[file][table]["delta2 [%]"]:
    #if el > 10**-5:
    print(el)


import arrayConversion
arrayConversion.adapter_ConvertPrefix(paket, "delta2 [%]", "delta2 [c%]")


for f in paket.tellMeFiles():
    for t in paket.tellMeTablesInFile(f):
        #print(paket.data[f][t]["delta2 [c%]"])
        paket.data[f][t].info()




x_axis = "V+ [V]" 

y_axes = ["P1 [uC/cm2]", "P2 [uC/cm2]"]

plots = {
    x_axis: y_axes

    }

plots

plots = {
    "E+ [V/cm]": ["P2 [uC/cm2]", "delta2 [%]"],
    "E- [V/cm]": ["P3 [uC/cm2]", "delta3 [%]"]
}


#from helperFunctions import newestSplit, splitMessage, checkedBoxes
paket.resetPlotSettings()
def changed(b):
    #i = splitMessage.index(b["owner"].description)
    checkedBoxes[b["owner"].description] = b["owner"].value
    global paket
    fileName = b["owner"].description
    truthValue = b["owner"].value
    paket.shouldIPlotFile(fileName, truthValue)
    print("\n========\n")
    print("{}: switched to {}".format(b["owner"].description, b["owner"].value))
    
    for i, key in enumerate(checkedBoxes):
        if key == b["owner"].description: break
    
    for chkBx2 in checkboxes2[i]:
        chkBx2.set(b["owner"].value)

def sub_changed(b):
    global paket
    table, file = b["owner"].description.split("|")
    print("Tbl: {} fl: {}".format(table, file))
    paket.shouldIPlotTables(file, table, b["owner"].value)
    print("\n========\n")
    print("{}: subswitched to {}".format(b["owner"].description, b["owner"].value))
    
from IPython.display import display
from ipywidgets import Checkbox

#print(contours)
checkboxes = []; checkboxes2 = []
checkedBoxes = {}
print(checkedBoxes)

for fileName in paket.tellMeFiles():
    checkboxes.append(Checkbox(True, description=str(fileName)))
    checkedBoxes[fileName] = True
    checkboxes2.append([])
    for table in paket.tellMeTablesInFile(file):
        checkboxes2[-1].append(Checkbox(True, description=table+"|"+fileName))
        #checkedBoxes[table+fileName] = True
        
for i, chkBx in enumerate(checkboxes):
    display(chkBx)
    chkBx.observe(changed, names=['value'])
    for chkBx2 in checkboxes2[i]:
        display(chkBx2)
        chkBx2.observe(sub_changed, names=['value'])
    
#TODO make a function that import/exports bool values to and from checkboxes


checkedBoxes


paket.plotFiles


desirable = [key for key in checkedBoxes if checkedBoxes[key]]
for x_axis in plots:
    for y_axis in plots[x_axis]:
        paket.plotData(x_axis, y_axis, desirable)



paket.exportToExcel()




