# %% [markdown]
# # The aixACCT Notebook

# %% [markdown]
# ## Table of contents
# - Simple example
#     1. Loading a file
#     2. Choosing an interesting column of the table
# - New example
#     1. Loading multiple files
#     2. Setting up plots (1 independent, many dependent variables)
#     3. Plotting the data from one file
#     4. Plotting the data from multiple files

# %%
%matplotlib widget
# This imports the functions I implemented
try:
    from improvedFunctions import loadFile
    print("Successfully loaded `loadFile` from `improvedFunctions`")
except:
    print("!!!!!!!!!!!!!")
    print("ERROR: Importing the package was NOT successful.")
# import pandas as pd

# %% [markdown]
# ### Simple example: 1. Select your file  
# We're using the `filedialog` from `tkinter` GUI; specifically the `askopenfilename()` function.

# %%
"""from tkinter import filedialog as fd
filename = fd.askopenfilename()
filename"""

# %%
firstFile = loadFile("C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS800_12h_10-150kVcm_RT.dat")

# You can see the keys (column headers) and values (the rest of the columns) separately
#namesOfVariables, measuredVariables = list(firstTable.keys()), list(firstTable.values())
len(firstFile)
for i, tableKey in enumerate(firstFile):
    print("Table #{} is called `{}`".format(i, tableKey))

# %% [markdown]
# ### Simple example: 2. From the output above, copy-paste the column title you find interesting
# This is how you take any table from the file into a variable

# %%
# Here are a few examples
firstTable = firstFile["Contour 1"]
firstTable.info()

# %% [markdown]
# This is how you take any column from the table into a variable:
# 
# Just copy paste the column name from above! (and put it in the square brackets)

# %%
time = firstTable["Time [s]"]
voltage = firstTable["V+ [V]"]
p1 = firstTable["P1 [uC/cm2]"]
john = firstTable["P2 [uC/cm2]"]
# You can name your variables however you want.
# But you need to copy paste the column titles from above
john 

# %% [markdown]
# As you can see above, it lists out all of the values in that column.  
# After that it tells you the columns name and length (how many values you have)  
# 

# %% [markdown]
#   
# Let's do that again for a different column

# %%
# You can type the name of any of the variables from above to see the values at that column
voltage

# %% [markdown]
# ### New example: 1. You can even load from multiple files at once, and store them together in a `list`:

# %%
# One way - manually write them out
# We can use relative paths, like so...
wantedFiles = [
    "../data\BSFO13_RS800_10-150kVcm_RT.dat",
    "../data\BSFO13_RS820_10-150kVcm_RT.dat"
]

# ... or absolute paths
wantedFiles = [
    "C:/Users/Uporabnik/Documents/Git projekti/ajzakt//data\BSFO13_RS800_10-150kVcm_RT.dat",
    "C:/Users/Uporabnik/Documents/Git projekti/ajzakt//data\BSFO13_RS820_10-150kVcm_RT.dat"
]

# %%
"""# The easiest method: GUI.
wantedFiles=fd.askopenfilenames()
wantedFiles"""

# %%
wantedFiles = ('C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS800_10-150kVcm_RT.dat',
 'C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS800_12h_10-150kVcm_RT.dat',
 'C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS820_10-150kVcm_RT.dat')

# %% [markdown]
# Then read data from each one of them, using a for loop (and store in a new variable `loadedTables`):

# %%
loadedTables = {}
for file in wantedFiles:
    loadedTables[file] = loadFile(file)

# %% [markdown]
# To access the table data (from this list of loaded files) - copy-paste the [file name] and [table title] you find interesting in square brackets

# %%
# Here's how we get it from the group
myVariable1 = loadedTables["C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS800_10-150kVcm_RT.dat"]["Contour 5"] #loadedTables["../data\BSFO13_RS800_10-150kVcm_RT.dat"]["V+ [V]"]
myVariable1.info()

# %% [markdown]
# Of course as a reminder - when you have a table in some variable (in this case `myVariable1`) just add square brackets with the name of the column you are interested in.  
# Run the cell below to confirm this.  
# Like always, feel free to play around with different values and see what gets outputted.  
# 
# 
# If any errors happen, you can Google them to get an explanation (probably on the *Stack Overflow* website) why that happened and how to avoid it.

# %%
myVariable1["I3 [A]"]

# %% [markdown]
# ### 2. Setting up interesting measurements for plotting
# Using Python dictionaries - key:value pairs (x axis: y axes)

# %%
# Independent variable
x_axis = "V+ [V]" 

# Dependent variables
y_axes = ["P1 [uC/cm2]", "P2 [uC/cm2]"]

# Pair them up
plots = {
    x_axis: y_axes
    # you can pair up another x axis here; then a ":"; then y_axes
    }

# Let's see what we have stored in memory
plots

# %% [markdown]
# ### 3. Plotting data from one file
# As a reminder, let's check which files we're loading the data from

# %%
wantedFiles # See the entire list

# %%
wantedFiles[0] # See the first element of the list

# %% [markdown]
# Let's plot from the first element of the list (in this case <sup><sub>`'C:/Users/Uporabnik/Documents/Git projekti/ajzakt/data/BSFO13_RS800_10-150kVcm_RT.dat'`</sub></sup>).  
# We are using the `plotData` method from my `helperFunctions.py` script.

# %% [markdown]
# Pro tip:  
# <sup><sub>
# To go through all independent variables (x axes) - we are using a `for` loop to go through `plots` variable  
# In this case, there is only one x_axis in the `plots` dictionary (so `for` loop has only one iteration)</sub></sup>

# %%
try:
    from helperFunctions import plotData
    print("Successfully loaded `plotData` from `helperFunctions`")
except:
    print("!!!!!!!!!!!!!")
    print("ERROR: Importing the package was NOT successful.")

# %%
loadedTables[wantedFiles[0]]

# %%
#from helperFunctions import plotData #TODO MAKE MORE ELEGANT PLOTS
for x_axis in plots:
    print(wantedFiles[0])
    plotData(loadedTables[wantedFiles[0]], x_axis, plots[x_axis], fileName=wantedFiles[0])

# %% [markdown]
# Let's repeat the same procedure for the second element of the list (in this case `../data\\BSFO13_RS820_10-150kVcm_RT.dat`)
# 
# For this one we will also demonstrate one new feature.

# %%
for x_axis in plots:
    print(wantedFiles[1])
    plotData(loadedTables[wantedFiles[1]], x_axis, plots[x_axis], fileName=wantedFiles[1])

# %% [markdown]
# ### 4. Printing only some contours
# 
# What if some of these contours are not interesting to us and we wish not to plot them with the interesting ones?
# 
# Run the cell below to get a list of contours and a checkbox to exclude irrelevant ones.

# %%
from helperFunctions import newestSplit, splitMessage, checkedBoxes

def changed(b):
    i = splitMessage.index(b["owner"].description)
    checkedBoxes[i] = b["owner"].value
    print("\n========\n")
    print("{}: switched to {}".format(b["owner"].description, b["owner"].value))

from IPython.display import display
from ipywidgets import Checkbox

#print(contours)
checkboxes = []
checkedBoxes = []
print(checkedBoxes)

for msg in splitMessage:
    checkboxes.append(Checkbox(True, description=str(msg)))
    checkedBoxes.append(True)

for chkBx in checkboxes:
    display(chkBx)
    chkBx.observe(changed, names=['value'])
    
#TODO make a function that import/exports bool values to and from checkboxes

# %%
checkedBoxes

# %%
# Alternative plotting from the third file
plotData(loadedTables[wantedFiles[2]], x_axis, ["D1 [nm]","D2 [nm]"], fileName=wantedFiles[2])

# %% [markdown]
# ### 5. Combine plot data from two different files
# You can also combine data from all of the files together on the same plot using the `plotMultiple()` function from my `helperFunctions.py` script.

# %%
plotMultiple(loadedTables, "V+ [V]", ["P1 [uC/cm2]", "P2 [uC/cm2]"])


