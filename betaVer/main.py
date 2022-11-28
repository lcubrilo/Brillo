from helperFunctions import loadTable, plotData

allMeasurements = loadTable("data/BSFO13_RS820_10-150kVcm_RT.dat")
namesOfVariables, measuredVariables = list(allMeasurements.keys()), list(allMeasurements.values())

print("START\n-----\nThe following measurements have been detected from the table: ")
for name in namesOfVariables:
    print("\t {} - {} entries".format(name, len(allMeasurements[name])))

# in terms of time
#plotData(allMeasurements, namesOfVariables[0], namesOfVariables[1:])

# in terms of pos/neg voltage
def axesForThisSpecificUseCase():
    global namesOfVariables
    plots = {
        "V+ [V]" : [],
        "V- [V]" : []
        }
    for name in namesOfVariables:
        if name[0] == 'I':
            continue
        elif name[1] == '3':
            plots["V- [V]"].append(name)
        elif name[1] == '2' or name[1] == '1':
            plots["V+ [V]"].append(name)
    return plots

plots = axesForThisSpecificUseCase()
for x_axis in plots:
    print("--------------\nPlotting the following data in terms of: {}".format(x_axis))
    for y_axis in plots[x_axis]:
        print("|\t", y_axis)

    plotData(allMeasurements, x_axis, plots[x_axis])