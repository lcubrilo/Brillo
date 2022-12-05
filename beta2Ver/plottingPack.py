import matploblib.pyplot as plt
class plotPlan():
    plotTypes = {
        "plot": plt.plot,
        "scatter": plt.scatter,
        "bar": plt.bar,
        "stem": plt.stem,
        "step": plt.step,
        "fill_between": plt.fill_between,
        "stackplot": plt.stackplot
    }

    def __init__(self, plotDict, plotType="plot"):
        self.plotDict = plotDict
        # self.fileName = fileName
        self.plotType = plotType
    
    @classmethod
    def fromLabels(cls, x_axis, y_axes, plotType="plot"):
        newDict = {}
        newDict[x_axis] = y_axes
        return cls(newDict, plotType)
    
    def showPlot(self, dataFrames):
        # Choose one of the plotting functions from pyplot - based on constructor's input
        plottingFunction =  self.plotTypes[self.plotType]

        # One independent axis will lead to one plot
        for x_axis in self.plotDict:
            # We will want to keep same plot plan for different files overlaid
            for dataFrame in dataFrames:
                y_axes = self.plotDict[x_axis]
                for y_axis in y_axes:
                    plottingFunction(dataFrame[x_axis], dataFrame[y_axis])
            plt.show()
            
