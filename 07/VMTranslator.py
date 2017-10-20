#!/usr/bin/python
import sys
# TODO:
# go line by line
# translate memory access (push/pop)
# translate arithmetic




##### NOTES #######
# static and temp are almost IDENTICAL
# TODO: REFACTOR

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
    return '@R' + (i + 5) + '\n' +\
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
           '@R' + (i + 5) + '\n' + \
           'M=D\n'


def translatePushPointer(i):
    return '@THAT' if i else '@THIS' + '\n' + \
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
           '@THAT' if i else '@THIS' + '\n' + \
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
        return translatePushTemp(i)
    
                
    segment = translateSegment(segment)
    return  '@'+segment + '\n'+ \
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
    return  '@'+segment + '\n'+ \
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
        return '@SP\n' + \
               'M=M-1\n' + \
               'A=M\n' + \
               'D=M\n' + \
               'A=A-1\n' + \
               'M=D+M\n'

    if(line == 'sub'):
        return '@SP\n' + \
               'M=M-1\n' + \
               'A=M\n' + \
               'D=M\n' + \
               'A=A-1\n' + \
               'M=D-M\n'

    if(line == 'neg'):
        return None

    if(line == 'eq'):
        return '@SP\n' + \
               'M=M-1\n'+ \
               'A=M\n' + \
               'D=M\n' + \
               'A=A-1\n' + \
               'D=D-M\n' + \
               '@eqLabel\n' +\
               'D;JNE\n' + \
               'D=0\n' + \
               '@eqFinish\n' + \
               '0; JMP\n' + \
               '(eqLabel)\n' + \
               'D=-1\n' + \
               '(eqFinish)\n' + \
               '@SP\n' + \
               'A=M-1\n' + \
               'M=D\n'
                

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
            outputFile.write("//" + line + "\n")
            outputFile.write(parsed + "\n")

    inputFile.close();
    outputFile.close();

if __name__ == "__main__":
    #main(sys.argv[1])
    print(translatePush('push local 5'))
