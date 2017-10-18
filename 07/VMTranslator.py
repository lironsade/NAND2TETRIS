#!/usr/bin/python
import sys
# TODO:
# go line by line
# translate memory access (push/pop)
# translate arithmetic
# ignore comments






#### parsing helpers ####
def isDoNothingLine(line):
    if line.startswith("//"):
        return True
    if line.startswith("("):
        return True
    return not(line)

def convertNumToBinary(num):
    return '{0:015b}'.format(int(num))

def parseDest(dest):
    return destTable.get(dest)

def parseJmp(jmp):
    return jmpTable.get(jmp)
        
def parseComp(comp):
    return compTable.get(comp)

def breakDownCInstruction(line):
    firstHalf = line.split('=')
    dest = None if len(firstHalf) == 1 else firstHalf[0]
    secondHalf = firstHalf[-1].split(';')
    comp = secondHalf[0]
    jmp = None if len(secondHalf) == 1 else secondHalf[1]
    return (dest, comp, jmp)

#### Translation ####
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

def translateCInstruction(line):
    dest, comp, jmp = breakDownCInstruction(line)
    return '111' + parseComp(comp) + parseDest(dest) + parseJmp(jmp)

def translateSegment(segment):
    if (segment == 'local'):
        return 'LCL'
    if (segment == 'argument'):
        return 'ARG'
    if (segment == 'this'):
        return 'THIS'
    if (segment == 'that'):
        return 'THAT'

def parseMemoryAccess(line):
    splitted = line.split(' ')
    # splitted 1 = segment, splitted 2 = i
    return splitted[1], splitted[2]


def translatePush(line):
    # addr = segmentPointer + i
    # *SP = *addr
    # SP++
    segment, i = parseMemoryAccess(line)
    if (segment == 'constant'):
        return '//' + line +'\n' + \
                '@'+ i +'\n'
                'D=A\n' + \
                '@SP\n' + \
                'A=M\n' + \
                'M=D\n' + \
                '@SP\n' + \
                'M=M+1\n'
    
                
    segment = translateSegment(segment)
    return  '//'+ line + '\n' + \
            '@'+segment + '\n'+ \
            'D=M\n'+ \
            '@' + i + '\n'+ \
            'A=D+A\n' + \
            'D=M\n' + \
            'A=M\n' + \
            'M=D\n' + \
            '@SP\n' + \
            'M=M+1\n'

def translatePop(line):
    # addr = segmentPointer + i
    # SP--
    # *addr = *SP
    segment, i = parseMemoryAccess(line)
    segment = translateSegment(segment)
    return  '//'+ line + '\n' + \
            '@'+segment + '\n'+ \
            'D=M\n'+ \
            '@' + i + '\n'+ \
            'D=D+A\n' + \
            '@SP\n' + \
            'A=M\n' + \
            'M=D\n' + \
            '@SP\n' + \
            'A=M\n' + \
            'A=A-1\n' + \
            'D=M\n' + \
            '@SP\n' + \
            'A=M\n' + \
            'M=D\n' + \
            '@SP\n' + \
            'M=M-1\n'



def translateArithmetic(line):
    if(line == 'add'):
        return None

    if(line == 'sub'):
        return None

    if(line == 'neg'):
        return None

    if(line == 'eq'):
        return None

    if(line == 'gt'):
        return None

    if(line == 'lt'):
        return None

    if(line == 'and'):
        return None

    if(line == 'or'):
        return None

    if(line == 'not'):
        return None



def parseLine(line):
    hasComment = line.find('//')
    if hasComment != -1:
        line = line[0:hasComment]
    line = line.strip()
    if not(line):
        return None

    if line.startswith("push"):
        return translatePop(line)

    if line.startswith("pop"):
        return translatePush(line)

    return translateArithmetic(line)

def main(inputFileName):
    inputFile = open(inputFileName, 'r')
    outputFile = open(inputFileName[:-3] + ".asm", 'w') # ignoring .vm
    for line in inputFile:
        parsed = parseLine(line)
        if parsed:
            outputFile.write(parsed + "\n")

    inputFile.close();
    outputFile.close();

if __name__ == "__main__":
    #main(sys.argv[1])
    print(translatePush('push local 5'))
