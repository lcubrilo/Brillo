import matplotlib.pyplot as plt

def forLoopSimple():
    for i in range(6):
        print(i)

def splitSimple():
    line = "This is my line. This is sentence 2, and 3."
    # print(line)
    print(line.split())

    for word in line.split():
        print(word)

Time, Vplus, Vminus, I1, P1, I2, P2, I3, P3, D1, D2, D3, CH3 = [], [], [], [], [], [], [], [], [], [], [], [], []
measuredVariables = [Time, Vplus, Vminus, I1, P1, I2, P2, I3, P3, D1, D2, D3, CH3]
namesOfVariables = []

with open("BSFO13_RS820_10-150kVcm_RT.dat") as f:
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

fig, axs = plt.subplots(3, 4) #TODO Magic value - how many plots we want
i=0
for nameOfValues, storageOfValues in zip(namesOfVariables[1:], measuredVariables[1:]): #TODO Magic value - what is x what is y axis
    i += 1
    axs[i%4-1][i//4].plot(Time, storageOfValues, label=nameOfValues+"]")
    #axs[i%4-1][i//4].plot(Time, storageOfValues, ylabel=nameOfValues+"]", xlabel=namesOfVariables[1]+"]")
    axs[i%4-1][i//4].legend()

plt.show()