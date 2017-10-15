import sys

#todo:
#1. Parse line
#2. Determine code
#3. Break down
#4. SymbolTable



def isDoNothingLine(line):
    if line.startswith("//"):
        return True
    if line.startswith("("):
        return True
    return not(line)

def convertNumToBinary(num):
    return '{0:015b}'.format(num)

def parseAInstruction(line):
    return '0' + convertNumToBinary(line[1:])

def breakDownCInstruction(line):
    firstHalf = line.split('=')
    dest = None if len(firstHalf) == 1 else firstHalf[0]
    secondHalf = firstHalf[-1].split(';')
    comp = secondHalf[0]
    jmp = None if len(secondHalf) == 1 else secondHalf[1]
    return (dest, comp, jmp)

def parseDest(dest):
    d1 = '1' if 'A' in dest else '0'
    d2 = '1' if 'D' in dest else '0'
    d3 = '1' if 'M' in dest else '0'
    return d1 + d2 + d3

def parseJmp(jmp):
    jmpTable = {
            null: '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
    }
    return jmpTable.get(jmp)
        
def parseComp(jmp):
    jmpTable = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
    }
    return jmpTable.get(jmp)

def parseCInstruction(line):
    dest, comp, jmp = breakDownCInstruction(line)
    return parseDest(dest) + parseComp(comp) + parseJmp(jmp)


def parseLine(line):
    line = line.strip()
    if isDoNothingLine(line):
        return null

    if line.startswith("@"):
        return parseAInstruction(line)

    return parseCInstruction(line)

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
