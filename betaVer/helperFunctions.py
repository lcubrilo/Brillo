import matplotlib.pyplot as plt

def loadTable(fileName, printData=False):
    with open(fileName) as f:
        i = 0
        for line in f:
            i += 1
            if printData:
                print(i, line)
            if i == 86: # TODO Magic value - which lines are useful to us
                allMeasurements = getMeasurementTypes(line)#namesOfVariables = line.split(']	'); continue
            if i < 87: 
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

def plotData(allMeasurements, x_axis, y_axes, printIndexes=False):
    n, m = determineGridDimension(len(y_axes))
    if printIndexes: print("Dimensions {}×{}".format(n,m))
    fig, axs = plt.subplots(n, m, squeeze=False) #TODO Magic value - how many plots we want
    i=0
    for measurement in y_axes: #TODO Magic value - what is x what is y axis
        x, y = i%n, i//n
        if printIndexes: print(i, "=>", x, y)
        axs[x][y].plot(allMeasurements[x_axis], allMeasurements[measurement], label=measurement)
        #axs[i%4-1][i//4].plot(Time, storageOfValues, ylabel=nameOfValues+"]", xlabel=namesOfVariables[1]+"]")
        axs[x][y].legend()
        i += 1

        print(x_axis, measurement)
        #for j in range(10):
        for j in range(len(allMeasurements[measurement])):
            #print(j)
            if abs(allMeasurements[x_axis][j]) < 10e-3:
                print("\t j. - ", allMeasurements[x_axis][j], allMeasurements[measurement][j])
            

    fig.suptitle("Measurements as a function of {}".format(x_axis))
    plt.show()
