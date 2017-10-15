
#todo:
#1. Parse line
#2. Determine code
#3. Break down
#4. SymbolTable



def isDoNothingLine(line):
    if line.startswith("//"):
        return true
    if line.startswith("("):
        return true
    return not(line)

def parseAInstruction(line):
    return null

def parseCInstruction(line):
    return null


def parseLine(line):
    line = line.strip()
    # do nothing line
    if isDoNothingLine(line):
        return null

    if line.startswith("@"):
        return parseAInstruction(line)

def main(inputFileName):
    inputFile = open(inputFileName, 'r')
    outputFile = open(inputFileName[:-4] + ".hack", 'w') # ignoring .asm
    symbolsTable = buildSymbolsTable(inputFile)
    for line in inputFile:
        parsed = parseLine(line)
        if parsed:
            outputFile.write(parsed + "\n")

    inputFile.close();
    outputFile.close();


if __name__ == "__main__":
    main(sys.argv[1])


