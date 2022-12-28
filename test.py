
def parseCode():
    with open("macroExample.txt", "r") as f:
        for line in f:
            if line[0] == "#" or line == "\n": continue

            start = line.find("(")
            end = line.rfind(")")

            args = line[start+1:end]
            args = args.split('", "')
            args[0] = args[0][1:]
            args[-1] = args[-1][:-1]
            

            if line.startswith("delete"):
                for arg in args:
                    print("Delete ", arg)

            elif line.startswith("convert"):
                input = args[0]
                output = args[1]

                if input.find("[") == -1: #constant convert:
                    constant = input
                    newPrefix = output[0]
                    print("Constant convert", constant, newPrefix)
                else:
                    print("Column convert", input, output)
            
            elif line.startswith("divide"):
                input = args[0]
                constant = args[1]
                output = args[2]
                print("Divide", input, constant, output)
            else:
                print("bruh")