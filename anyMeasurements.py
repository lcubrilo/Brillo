import matplotlib.pyplot as plt

def loadTable(fileName):
    with open(fileName) as f:
        i = 0
        for line in f:
            i += 1; print(i, line)
            if i == 86: # TODO Magic value - which lines are useful to us
                allMeasurements = getMeasurementTypes(line)#namesOfVariables = line.split(']	'); continue
            if i < 87:
                #print(i, "alo") 
                continue

            lineData = line.split("	")
            for dataToEnter, measurement in zip(lineData, allMeasurements):
                try:
                    allMeasurements[measurement].append(float(dataToEnter))
                except:
                    break
    
    return allMeasurements

def getMeasurementTypes(line):
    allMeasurements = {}
    for measur in line.strip().split("	"):
        allMeasurements[measur] = []
    return allMeasurements
    Time, Vplus, Vminus, I1, P1, I2, P2, I3, P3, D1, D2, D3, CH3 = [], [], [], [], [], [], [], [], [], [], [], [], []
    measuredVariables = [Time, Vplus, Vminus, I1, P1, I2, P2, I3, P3, D1, D2, D3, CH3]
    namesOfVariables = []

    retVal = {}
    for nam, val in zip(namesOfVariables, measuredVariables):
        retVal[nam] = val;

def determineGridDimension(numOfSublots):
    n = int(numOfSublots**0.5); m=n
    while n*m < numOfSublots:
        m+=1
    return n, m

def plotData(namesOfVariables, measuredVariables):
    n, m = determineGridDimension(len(namesOfVariables))
    fig, axs = plt.subplots(n, m) #TODO Magic value - how many plots we want
    i=0
    for nameOfValues, storageOfValues in zip(namesOfVariables[1:], measuredVariables[1:]): #TODO Magic value - what is x what is y axis
        i += 1
        axs[i%4-1][i//4].plot(measuredVariables[0], storageOfValues, label=nameOfValues+"]")
        #axs[i%4-1][i//4].plot(Time, storageOfValues, ylabel=nameOfValues+"]", xlabel=namesOfVariables[1]+"]")
        axs[i%4-1][i//4].legend()

    fig.suptitle("Measurements as a function of time")
    plt.show()

allMeasurements = loadTable("BSFO13_RS820_10-150kVcm_RT.dat")
namesOfVariables, measuredVariables = list(allMeasurements.keys()), list(allMeasurements.values())

print("The following measurements have been detected from the table: ")
for name in namesOfVariables:
    print("\t {} - {} entries".format(name, len(allMeasurements[name])))

plotData(namesOfVariables, measuredVariables)