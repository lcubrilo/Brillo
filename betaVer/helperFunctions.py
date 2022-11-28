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

def testSplitting(allMeasurements, x_axis, y_axes, printIndexes=False):
    print(x_axis, y_axes[0])
    print("\n\n----SPLIT--------------\n\n")
    
    x_splitted, y_splitted = splitData(allMeasurements[x_axis], allMeasurements[y_axes[0]])
    for section in x_splitted:
        print(section, "\n\n-------------------\n")

def splitData(x_axis, y_axis):
    x_old = 0; k = 0
    x_splits, y_splits = [], []

    #for x in x_axis:
    for x, y in zip(x_axis, y_axis):
        if int(x) * int(x_old) < 0 and int(y) < 0: # We passed the 0 mark
            x_splits.append(x_axis[:k]) 
            x_axis = x_axis[k:]

            y_splits.append(y_axis[:k])
            y_axis = y_axis[k:]

            x_old = 0; k = 0

        x_old = x
        k += 1
    
    return x_splits, y_splits

def plotData(allMeasurements, x_axis, y_axes, printIndexes=False, shouldSplit=True):
    n, m = determineGridDimension(len(y_axes))
    if printIndexes: print("Dimensions {}×{}".format(n,m))
    fig, axs = plt.subplots(n, m, squeeze=False) #TODO Magic value - how many plots we want
    i=0
    for measurement in y_axes: #TODO Magic value - what is x what is y axis
        x, y = i%n, i//n


        if printIndexes:
            print(i, "=>", x, y)


        if shouldSplit:
            x_splitted, y_splitted = splitData(allMeasurements[x_axis], allMeasurements[measurement])
        else:
            x_splitted, y_splitted = [allMeasurements[x_axis]], [allMeasurements[measurement]]
        

        for x_section, y_section in zip(x_splitted, y_splitted):
            axs[x][y].plot(x_section, y_section)
        
        axs[x][y].set_ylabel(measurement)
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
