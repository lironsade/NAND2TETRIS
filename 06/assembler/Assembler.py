#!/usr/bin/python
import sys

#######################
# hack language tables#
#######################
destTable = {
    None: "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jmpTable = {
        None: '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
}

compTable = {
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

#######################

######################
#  global variable   #
######################
global freeAddress
global symbolsTable


def isDoNothingLine(line):
    if line.startswith("//"):
        return True
    if line.startswith("("):
        return True
    return not(line)

def convertNumToBinary(num):
    return '{0:015b}'.format(int(num))

def translateAInstruction(line):
    global symbolsTable
    global freeAddress
    variable = line[1:]
    if variable.isdigit():
        return '0' + convertNumToBinary(variable)
    if variable not in symbolsTable:
        symbolsTable[variable] = freeAddress
        freeAddress += 1
    return '0' + convertNumToBinary(symbolsTable[variable])

def breakDownCInstruction(line):
    firstHalf = line.split('=')
    dest = None if len(firstHalf) == 1 else firstHalf[0]
    secondHalf = firstHalf[-1].split(';')
    comp = secondHalf[0]
    jmp = None if len(secondHalf) == 1 else secondHalf[1]
    return (dest, comp, jmp)

def parseDest(dest):
    return destTable.get(dest)

def parseJmp(jmp):
    return jmpTable.get(jmp)
        
def parseComp(comp):
    return compTable.get(comp)

def translateCInstruction(line):
    dest, comp, jmp = breakDownCInstruction(line)
    return '111' + parseComp(comp) + parseDest(dest) + parseJmp(jmp)


def parseLine(line):
    hasComment = line.find('//')
    if hasComment != -1:
        line = line[0:hasComment]
    line = line.strip()
    if isDoNothingLine(line):
        return None

    if line.startswith("@"):
        return translateAInstruction(line)

    return translateCInstruction(line)

def buildSymbolsTable(inputFile):
    global symbolsTable
    symbolsTable = {
        "R0": "0",
        "R1": "1",
        "R2": "2",
        "R3": "3",
        "R4": "4",
        "R5": "5",
        "R6": "6",
        "R7": "7",
        "R8": "8",
        "R9": "9",
        "R10": "10",
        "R11": "11",
        "R12": "12",
        "R13": "13",
        "R14": "14",
        "R15": "15",
        "SCREEN": "16384",
        "KBD": "24576",
        "SP": "0",
        "LCL": "1",
        "ARG": "2",
        "THIS": "3",
        "THAT": "4",
    }

    # first pass
    lineNum = 0
    for line in inputFile:
        line = line.strip()
        if line.startswith('('):
            symbolsTable[line[1:-1]] = lineNum
        if not isDoNothingLine(line):
            lineNum += 1

    inputFile.seek(0)

def main(inputFileName):
    inputFile = open(inputFileName, 'r')
    outputFile = open(inputFileName[:-4] + ".hack", 'w') # ignoring .asm
    buildSymbolsTable(inputFile)
    global freeAddress
    freeAddress = 16
    for line in inputFile:
        parsed = parseLine(line)
        if parsed:
            outputFile.write(parsed + "\n")

    inputFile.close();
    outputFile.close();

if __name__ == "__main__":
    main(sys.argv[1])
