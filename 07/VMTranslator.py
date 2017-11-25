#!/usr/bin/python
import sys
import os
# TODO:
# go line by line
# translate arithmetic
# translate memory access (push/pop)




##### NOTES #######
# TODO: REFACTOR
global counter

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

def translatePushConstant(i):
    return '@'+ i +'\n' + \
           'D=A\n' + \
           '@SP\n' + \
           'A=M\n' + \
           'M=D\n' + \
           '@SP\n' + \
           'M=M+1\n'

def translatePushStatic(i):
    return '@Foo.' + i + '\n' + \
           'D=M\n' + \
           '@SP\n' + \
           'A=M\n' + \
           'M=D\n' + \
           '@SP\n' + \
           'M=M+1\n'

def translatePopStatic(i):
    return '@SP\n' +\
           'M=M-1\n' + \
           'A=M\n' + \
           'D=M\n' + \
           '@Foo.' + i + '\n' + \
           'M=D\n'

def translatePushTemp(i):
    return '@R' + str(int(i) + 5) + '\n' +\
           'D=M\n' + \
           '@SP\n' + \
           'A=M\n' + \
           'M=D\n' + \
           '@SP\n' + \
           'M=M+1\n'

def translatePopTemp(i):
    return '@SP\n' +\
           'M=M-1\n' + \
           'A=M\n' + \
           'D=M\n' + \
           '@R' + str(int(i) + 5) + '\n' + \
           'M=D\n'


def translatePushPointer(i):
    return ('@THAT\n' if int(i) else '@THIS\n') + \
           'D=M\n' + \
           '@SP\n' + \
           'A=M\n' + \
           'M=D\n' + \
           '@SP\n' + \
           'M=M+1\n'

def translatePopPointer(i):
    return '@SP\n' +\
           'M=M-1\n' + \
           'A=M\n' + \
           'D=M\n' + \
           ('@THAT\n' if int(i) else '@THIS\n') + \
           'M=D\n'

def translatePush(line):
    # addr = segmentPointer + i
    # *SP = *addr
    # SP++
    segment, i = parseMemoryAccess(line)
    if (segment == 'constant'):
        return translatePushConstant(i)
    if (segment == 'static'):
        return translatePushStatic(i)
    if (segment == 'temp'):
        return translatePushTemp(i)
    if (segment == 'pointer'):
        return translatePushPointer(i)
    segment = translateSegment(segment)
    return  '@'+segment + '\n'+ \
            'D=M\n'+ \
            '@' + i + '\n'+ \
            'A=D+A\n' + \
            'D=M\n' + \
            '@SP\n' + \
            'A=M\n' + \
            'M=D\n' + \
            '@SP\n' + \
            'M=M+1\n'

def translatePop(line):
    # addr = segmentPointer + i
    # SP--
    # *addr = *SP
    segment, i = parseMemoryAccess(line)
    if (segment == 'static'):
        return translatePopStatic(i)
    if (segment == 'temp'):
        return translatePopTemp(i)
    if (segment == 'pointer'):
        return translatePopPointer(i)
    segment = translateSegment(segment)
    return  '@'+segment + '\n'+ \
            'D=M\n'+ \
            '@' + i + '\n'+ \
            'D=D+A\n' + \
            '@R13\n' + \
            'M=D\n' + \
            '@SP\n' + \
            'M=M-1\n' + \
            'A=M\n' + \
            'D=M\n' + \
            '@R13\n' + \
            'A=M\n' + \
            'M=D\n'


def handleEquality(jmp):
    global counter
    counter += 1
    return "@SP\n" + \
           "M=M-1\n" + \
           "A=M\n" + \
           "D=M\n" + \
           "@R13\n" + \
           "M=D\n" + \
           "@gMinus" + str(counter) + "\n" + \
           "D;JLT\n" + \
           "@SP\n" + \
           "M=M-1\n" + \
           "A=M\n" + \
           "D=M\n" + \
           "@gPlusFMinus" + str(counter) + "\n" + \
           "D;JLT\n" + \
           "@R13\n" + \
           "D=D-M\n" + \
           "@CONTROL" + str(counter) + "\n" + \
           "0;JMP\n" + \
           "(gMinus" + str(counter) + ")\n" + \
           "@SP\n" + \
           "M=M-1\n" + \
           "A=M\n" + \
           "D=M\n" + \
           "@gMinusFPlus" + str(counter) + "\n" + \
           "D;JGT\n" + \
           "@R13\n" + \
           "D=D-M\n" + \
           "@CONTROL" + str(counter) + "\n" + \
           "0;JMP\n" + \
           "(gPlusFMinus" + str(counter) + ")\n" + \
           "D=-1\n" + \
           "@CONTROL" + str(counter) + "\n" + \
           "0;JMP\n" + \
           "(gMinusFPlus" + str(counter) + ")\n" + \
           "D=1\n" + \
           "@CONTROL" + str(counter) + "\n" + \
           "0;JMP\n" + \
           "(CONTROL" + str(counter) + ")\n" + \
           "@ISTRUE" + str(counter) + "\n" + \
           "D;" + jmp + "\n" + \
           "D=0\n" + \
           "@FINISH" + str(counter) + "\n" + \
           "0;JMP\n" + \
           "(ISTRUE" + str(counter) + ")\n" + \
           "D=-1\n" + \
           "@FINISH" + str(counter) + "\n" + \
           "0;JMP\n" + \
           "(FINISH" + str(counter) + ")\n" + \
           "@SP\n" + \
           "A=M\n" + \
           "M=D\n" + \
           "@SP\n" + \
           "M=M+1\n"


def translateArithmetic(line):


    if(line == 'eq'):
        return handleEquality('JEQ')


    if(line == 'gt'):
        return handleEquality('JGT')

    if(line == 'lt'):
        return handleEquality('JLT')

    if(line == 'add'):
        return '@SP\n' + \
               'M=M-1\n' + \
               'A=M\n' + \
               'D=M\n' + \
               'A=A-1\n' + \
               'M=M+D\n'

    if(line == 'sub'):
        return '@SP\n' + \
               'M=M-1\n' + \
               'A=M\n' + \
               'D=M\n' + \
               'A=A-1\n' + \
               'M=M-D\n'

    if(line == 'and'):
        return '@SP\n' +\
               'M=M-1\n' +\
               'A=M\n' +\
               'D=M\n' +\
               'A=A-1\n' +\
               'M=M&D\n'


    if(line == 'or'):
        return '@SP\n' + \
               'M=M-1\n' + \
               'A=M\n' + \
               'D=M\n' + \
               'A=A-1\n' + \
               'M=M|D\n'

    if(line == 'neg'):
        return '@SP\n' + \
               'A=M-1\n' + \
               'M=-M\n'

    if(line == 'not'):
        return '@SP\n' + \
               'A=M-1\n' + \
               'M=!M\n'



def parseLine(line):
    hasComment = line.find('//')
    if hasComment != -1:
        line = line[0:hasComment]
    line = line.strip()
    if not(line):
        return None

    if line.startswith("push"):
        return translatePush(line)

    if line.startswith("pop"):
        return translatePop(line)

    return translateArithmetic(line)

def main(inputFileName):
    global counter
    counter = 0
    inputFile = open(inputFileName, 'r')
    outputFile = open(inputFileName[:-3] + ".asm", 'w') # ignoring .vm
    for line in inputFile:
        parsed = parseLine(line)
        if parsed:
            outputFile.write("//" + line + "\n")
            outputFile.write(parsed + "\n")

    inputFile.close()
    outputFile.close()

if __name__ == "__main__":
    if os.path.isdir(sys.argv[1]):
        for filename in os.listdir(sys.argv[1]):
            if filename.endswith(".vm"):
                main(sys.argv[1] + "/" + filename)
    else:
        main(sys.argv[1])
