from dataManipulation import getValue

def fileToStr(fileName):
    print("Loading file {}".format(fileName))
    lines = ""
    with open(fileName) as f:
        for line in f:
            lines += line

    return lines

def sectionTheFile(lines, printSummary):
    sections = lines.split("Table ")

    title = sections[0].strip()

    summarySection = sections[2]
    summaryLines = summarySection.split("\n")

    if printSummary:
        print("Title: {}\n==============\nSummary table:".format(title))
        for line in summaryLines:
            print(line)
    
    return sections[3:]

def loadSubTable(section):
    index = section.index("Measurement Status: 0")
    
    dataBeforeTable = section[:index]
    
    area = getValue(dataBeforeTable, "Area [mm2]")

    thickness = getValue(dataBeforeTable, "Thickness [nm]")
    thickness = float(thickness[0])

    table = section[index:]
    print(table)
    

def loadFile(fileName, printSummary = False):
    lines = fileToStr(fileName)

    sections = sectionTheFile(lines, printSummary)

    for section in sections:
        loadSubTable(section)

            
#loadFile("data/BSFO13_RS800_12h_10-150kVcm_RT.dat")
            