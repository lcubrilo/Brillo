import matplotlib.pyplot as plt
from math import ceil, floor

import itertools

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


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
        if int(x) * int(x_old) < 0 and int(y) > 0: # We passed the 0 mark
            #print(x, y)
            x_splits.append(x_axis[:k]) 
            x_axis = x_axis[k:]

            y_splits.append(y_axis[:k])
            y_axis = y_axis[k:]

            x_old = 0; k = 0

        x_old = x
        k += 1
    
    return x_splits, y_splits

def distances(x_axis, y_axis, shouldIRound = True,  showEuclidean=False):
    if len(x_axis) != len(y_axis):
        raise Exception("Nisu jednake ose. x - {}, y - {}".format(len(x_axis), len(y_axis)))
    else: 
        n = len(x_axis)

    distances = []
    def euclideanDistance(A, B):
        deltaX = A[0] - B[0]
        deltaY = A[1] - B[1]
        return (deltaX**2 + deltaY**2)**0.5

    for i in range(n-1):
        A = [x_axis[i], y_axis[i]]
        B = [x_axis[i+1], y_axis[i+1]]
        distances.append(euclideanDistance(A, B))
    
    if showEuclidean:
        #Distances je niz udaljenosti susednih tacaka
        coef = distances[-1]/distances[1]
        #distances = [coef*distances[i]/i**0.4 for i in range(1, len(distances))]

        fig, axs = plt.subplots()
        axs.scatter(range(n-1), distances)
        # f(x) (gde je x broj reda u tabeli tj index tačke) = euklidska udaljenost od tačke x+1

    # Show when it is positive and when it is negative
    """maxx, minn = max(distances), min(distances)
    axs.scatter([el+0.5 for el in range(n)], [maxx if el > 0 else minn for el in x_axis])"""

    x_splitted, y_splitted = splitData(x_axis, y_axis)
    if showEuclidean:
        axs.set_title("There are {} detected disjunct subarrays using the NAP method".format(len(x_splitted)))

    # Show sign changes with vertical lines
    gottenIndeces = getIndeces(x_splitted, y_splitted)
    for el in gottenIndeces:
        if showEuclidean: plt.axvline(x = el, color = 'b', label = 'promena znaka')
    
    offsetted = guessOppositeIndeces(getIndeces(x_splitted, y_splitted))
    for el in offsetted:
        if showEuclidean: plt.axvline(x = el, color = 'r', label = 'pi offset')


    # Pick the one that actually hits the peaks
    try:
        firstTerm = distances[gottenIndeces[-2]]
        secondTerm = distances[offsetted[-2]]
    except:
        firstTerm = -len(gottenIndeces); secondTerm = -len(offsetted)
    if firstTerm < secondTerm :
        chosenIndeces = gottenIndeces
    else:
        chosenIndeces = offsetted

    interpolated = interpolateRemaining(chosenIndeces)
    for el in interpolated:
        if showEuclidean: plt.axvline(x = el, color = 'g', label = 'interpolated')

    if showEuclidean:
        plt.plot()

    return interpolated
    #return distances if not shouldIRound else [round(el, 2) for el in distances]

def interpolateRemaining(indeces):
    # sanity check
    valueOccurence = {}
    for el in getDifferences(indeces):
        if el in valueOccurence:
            valueOccurence[el] += 1
        else:
            valueOccurence[el] = 1
    
    if len(valueOccurence) > 2:
        raise Exception("Kako molim. {}".format(valueOccurence))
    
    # Take the more common one
    period = -1; currMax = -1
    for el in valueOccurence:
        if valueOccurence[el] > currMax:
            period = el; currMax = valueOccurence[el]
    
    # This is all unnecessary if the following holds true: only the index 0 is larger, the rest are equal
    # We will assume that from this point on

    retVal = indeces[1:]
    tmp = retVal[0]
    while True:
        if tmp < 0:
            return sorted(retVal)[1:]
        tmp -= period
        retVal.append(tmp)

"""def interpolateRemaining(indeces, tolerance=10):
    differences = getDifferences(indeces); avg = sum(differences)/len(differences)
    
    retVal = []
    prev = indeces[-1]
    for i in range(len(indeces)-2, 1, -1):
        curr = indeces[i-1]

        retVal.append(curr)
        tmp = prev
        #beyond +- tolerance% from average
        while abs(prev-curr) > avg*(1+tolerance/100) or abs(prev-curr) < avg*(1-tolerance/100): 
            if tmp < 0: break
            tmp -= avg
            retVal.append(tmp)
            prev = tmp
        
        prev = curr
    
    return retVal"""

def getDifferences(indeces):
    retVal = []
    for i in range(1, len(indeces)):
        retVal.append(indeces[i]-indeces[i-1])
    return retVal

def getIndeces(x_splits, y_splits):
    index = 0
    retVal = []
    for el in x_splits:
        retVal.append(index)
        index += len(el)
    return retVal

def guessOppositeIndeces(indeces):
    if len(indeces) == 0:
        return []
    if indeces[0] != 0:
        raise Exception("Expected 0 in the beginning. {}".format(indeces))

    retVal = []
    for i in range(1, len(indeces)):
        retVal.append((indeces[i]+indeces[i-1])/2)
    
    return [floor(el) for el in retVal[1:]]

"""
def ruptures(x, y, n):
    import numpy as np
    y = np.array(y)
    import ruptures as rpt
    model = rpt.Dynp(model="l1")
    model.fit(y)
    breaks = model.predict(n_bkps=n-1 if n > 0 else 0)
    return breaks"""

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
            indeces = distances(allMeasurements[x_axis], allMeasurements[measurement])
            def newSplit(array, indeces): return [array[a:b] for a,b in pairwise(indeces)]
            x_splitted = newSplit(allMeasurements[x_axis], indeces)
            y_splitted = newSplit(allMeasurements[measurement], indeces)
            
            #x_splitted, y_splitted = splitData(allMeasurements[x_axis], allMeasurements[measurement])
            """lenx, leny = len(x_splitted), len(y_splitted)
            if len(x_splitted) != len(y_splitted):
                raise Exception("Koj kur. len(x)={}, len(y)={}".format(lenx, leny))
            my = getIndeces(x_splitted, y_splitted)
            rup = ruptures(allMeasurements[x_axis], allMeasurements[measurement], len(x_splitted))
            print("\n MY DETECTION: {}\n-----------------\n RUPTURES: {}\n---------------".format(my, rup))"""
        else:
            x_splitted, y_splitted = [allMeasurements[x_axis]], [allMeasurements[measurement]]

        for x_section, y_section in zip(x_splitted, y_splitted):
            #axs[x][y].scatter(x_section, y_section, s=5) #gives dotted appearance
            axs[x][y].plot(x_section, y_section) #connects lines
        
        axs[x][y].set_ylabel(measurement)
        #axs[i%4-1][i//4].plot(Time, storageOfValues, ylabel=nameOfValues+"]", xlabel=namesOfVariables[1]+"]")
        #axs[x][y].legend()

        i += 1
        #plt.show()

        #raise Exception("Lol")
        print(x_axis, measurement)
        #for j in range(10):
        for j in range(len(allMeasurements[measurement])):
            #print(j)
            if abs(allMeasurements[x_axis][j]) < 10e-3:
                print("\t j. - ", allMeasurements[x_axis][j], allMeasurements[measurement][j])
        
        

    fig.suptitle("Measurements as a function of {}".format(x_axis))
    plt.show()
