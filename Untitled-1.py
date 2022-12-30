str = ""
with open("temperature.txt") as f:
    for line in f:
        str += line.replace(". ", ", ")

#str = "[" + str[:-2] + "]"
with open("temperature.txt", "w") as f:
    f.write(str)
