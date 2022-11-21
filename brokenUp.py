import matplotlib.pyplot as plt

def loadTable(fileName):
    Time, Vplus, Vminus, I1, P1, I2, P2, I3, P3, D1, D2, D3, CH3 = [], [], [], [], [], [], [], [], [], [], [], [], []
    measuredVariables = [Time, Vplus, Vminus, I1, P1, I2, P2, I3, P3, D1, D2, D3, CH3]
    namesOfVariables = []

    with open(fileName) as f:
        i = 0
        for line in f:
            i += 1; print(i, line)
            if i == 86: # TODO Magic value - which lines are useful to us
                namesOfVariables = line.split(']	'); continue
            if i < 87:
                #print(i, "alo") 
                continue

            for readData, storageOfValues in zip(line.split(), measuredVariables):
                try:
                    storageOfValues.append(float(readData))
                except:
                    break
    
    return namesOfVariables, measuredVariables

def getMeasurementTypes():
    Time, Vplus, Vminus, I1, P1, I2, P2, I3, P3, D1, D2, D3, CH3 = [], [], [], [], [], [], [], [], [], [], [], [], []
    measuredVariables = [Time, Vplus, Vminus, I1, P1, I2, P2, I3, P3, D1, D2, D3, CH3]
    namesOfVariables = []

    retVal = {}
    for nam, val in zip(namesOfVariables, measuredVariables):
        retVal[nam] = val;

def plotData(namesOfVariables, measuredVariables):
    fig, axs = plt.subplots(3, 4) #TODO Magic value - how many plots we want
    i=0
    for nameOfValues, storageOfValues in zip(namesOfVariables[1:], measuredVariables[1:]): #TODO Magic value - what is x what is y axis
        i += 1
        axs[i%4-1][i//4].plot(measuredVariables[0], storageOfValues, label=nameOfValues+"]")
        #axs[i%4-1][i//4].plot(Time, storageOfValues, ylabel=nameOfValues+"]", xlabel=namesOfVariables[1]+"]")
        axs[i%4-1][i//4].legend()

    plt.show()

namesOfVariables, measuredVariables = loadTable("BSFO13_RS820_10-150kVcm_RT.dat")

plotData(namesOfVariables, measuredVariables)

plt.show()