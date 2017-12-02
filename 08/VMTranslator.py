#!/usr/bin/python
import sys
import os


global counter
global function_name

#TODO:
# label
# function call
# function return
# goto
# if-goto

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

def translatePushStatic(i, base_name):
    return '@' + base_name + "." + str(i) + '\n' + \
           'D=M\n' + \
           '@SP\n' + \
           'A=M\n' + \
           'M=D\n' + \
           '@SP\n' + \
           'M=M+1\n'

def translatePopStatic(i, base_name):
    return '@SP\n' +\
           'M=M-1\n' + \
           'A=M\n' + \
           'D=M\n' + \
           '@' + base_name + "." + str(i) + '\n' + \
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

def translatePush(line, base_name):
    # addr = segmentPointer + i
    # *SP = *addr
    # SP++
    segment, i = parseMemoryAccess(line)
    if (segment == 'constant'):
        return translatePushConstant(i)
    if (segment == 'static'):
        return translatePushStatic(i, base_name)
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

def translatePop(line, base_name):
    # addr = segmentPointer + i
    # SP--
    # *addr = *SP
    segment, i = parseMemoryAccess(line)
    if (segment == 'static'):
        return translatePopStatic(i, base_name)
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
    part1 ="@SP\n" + \
           "M=M-1\n" + \
           "A=M\n" + \
           "D=M\n" + \
           "@R13\n" + \
           "M=D\n"

    part2 = "@gMinus" + str(counter) + "\n" + \
           "D;JLT\n" + \
           "@SP\n" + \
           "M=M-1\n" + \
           "A=M\n" + \
           "D=M\n" + \
           "@gPlusFMinus" + str(counter) + "\n" + \
           "D;JLT\n"

    part3 = "@R13\n" + \
           "D=D-M\n" + \
           "@CONTROL" + str(counter) + "\n" + \
           "0;JMP\n" + \
           "(gMinus" + str(counter) + ")\n" + \
           "@SP\n" + \
           "M=M-1\n" + \
           "A=M\n" + \
           "D=M\n" + \
           "@gMinusFPlus" + str(counter) + "\n" + \
           "D;JGT\n"

    part4 ="@R13\n" + \
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
           "0;JMP\n"

    part5 ="(CONTROL" + str(counter) + ")\n" + \
           "@ISTRUE" + str(counter) + "\n" + \
           "D;" + jmp + "\n" + \
           "D=0\n" + \
           "@FINISH" + str(counter) + "\n" + \
           "0;JMP\n" + \
           "(ISTRUE" + str(counter) + ")\n" + \
           "D=-1\n" + \
           "@FINISH" + str(counter) + "\n" + \
           "0;JMP\n"

    part6 ="(FINISH" + str(counter) + ")\n" + \
           "@SP\n" + \
           "A=M\n" + \
           "M=D\n" + \
           "@SP\n" + \
           "M=M+1\n"
    return part1 + part2 + part3 + part4 + part5 + part6

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

def translateLabel(line):
    global function_name
    label = line.split(' ')[1]
    return '(' + function_name + '$' + label + ')\n'

def translateGoto(line):
    global function_name
    label = line.split(' ')[1]
    return  '@' + function_name + '$' + label + '\n' + \
            '0;JMP\n'

def translateIfGoto(line):
    global function_name
    label = line.split(' ')[1]
    return  '@SP\n' + \
            'M=M-1\n' + \
            'A=M\n' + \
            'D=M\n' + \
            '@' + function_name + '$' + label + '\n' + \
            'D;JNE\n'

def translateCall(line):
    global function_name
    global counter
    name, nargs = line.split()[1:3]
    counter += 1
    return_address = '@RETURNTO' + str(counter) + '\n' + \
                     'D=A\n' + \
                     '@SP\n' + \
                     'A=M\n' + \
                     'M=D\n' + \
                     '@SP\n' + \
                     'M=M+1\n'
    pushes = ''
    for segment in ['LCL', 'ARG', 'THIS', 'THAT']:
        pushes += '@' + segment +' \n' + \
                 'D=M\n' + \
                 '@SP\n' + \
                 'A=M\n' + \
                 'M=D\n' + \
                 '@SP\n' + \
                 'M=M+1\n'

    the_jump = '@SP\n' + \
               'D=M\n' + \
               '@' + str(int(nargs) + 5) + '\n' + \
               'D=D-A\n' + \
               '@ARG\n' + \
               'M=D\n' + \
               '@SP\n' + \
               'D=M\n' + \
               '@LCL\n' + \
               'M=D\n' + \
               '@' + name + '\n' + \
               '0;JMP\n' + \
               '(RETURNTO' + str(counter) + ')\n'

    return return_address + pushes + the_jump


def translateReturn(line):
    global function_name
    pops = ''
    for i, segment in enumerate(['THAT', 'THIS', 'ARG', 'LCL']):
        pops += '@13\n' + \
                'D=M\n' + \
                '@' + str(i+1) + '\n' + \
                'A=D-A\n' + \
                'D=M\n' + \
                '@' + segment + '\n' + \
                'M=D\n'

    ret_v = '@LCL\n' + \
        'D=M\n' + \
        '@13\n' + \
        'MD=D\n' + \
        '@5\n' + \
        'A=D-A\n' + \
        'D=M\n' + \
        '@14\n' + \
        'M=D\n' + \
        '@SP\n' + \
        'M=M-1\n' + \
        '@SP\n' + \
        'A=M\n' + \
        'D=M\n' + \
        '@ARG\n' + \
        'A=M\n' + \
        'M=D\n' + \
        '@ARG\n' + \
        'D=M+1\n' + \
        '@SP\n' + \
        'M=D\n' + \
         pops + \
        '@14\n' + \
        'A=M\n' + \
        '0;JMP\n'
    return ret_v

def writeInit():
    first = '@256\n' + \
            'D=A\n' + \
            '@SP\n' + \
            'M=D\n'
    return first + translateCall('call Sys.init 0')

def translateFunction(line):
    global function_name
    name, nargs = line.split()[1:3]
    function_name = name
    label = '(' + name + ')\n'
    pushes = ''
    zero_push = '@SP\n' + \
                'A=M\n' + \
                'M=0\n' + \
                '@SP\n' + \
                'M=M+1\n'
    for i in range(int(nargs)):
        pushes += zero_push
    return label + pushes



def parseLine(line, base_name):
    hasComment = line.find('//')
    if hasComment != -1:
        line = line[0:hasComment]
    line = line.strip()
    if not(line):
        return None
    if line.startswith("push"):
        return translatePush(line, base_name)
    elif line.startswith("pop"):
        return translatePop(line, base_name)
    elif line.startswith("label"):
        return translateLabel(line)
    elif line.startswith("goto"):
        return translateGoto(line)
    elif line.startswith("if-goto"):
        return translateIfGoto(line)
    elif line.startswith("call"):
        return translateCall(line)
    elif line.startswith("return"):
        return translateReturn(line)
    elif line.startswith("function"):
        return translateFunction(line)
    return translateArithmetic(line)

def main(inputFileName, outputFileName):
    global function_name
    function_name = ''
    base_name = os.path.basename(inputFileName)[:-3]
    inputFile = open(inputFileName, 'r')
    outputFile = open(outputFileName, 'a')
    for line in inputFile:
        parsed = parseLine(line, base_name)
        if parsed:
            outputFile.write("//" + line + "\n")
            outputFile.write(parsed + "\n")

    inputFile.close()
    outputFile.close()

if __name__ == "__main__":
    global counter
    counter = 0
    path = sys.argv[1]
    if os.path.isdir(path):
        if path.endswith("/"):
            path = path[0:-1]
        directory = os.path.basename(path)
        outputFileName = path + "/" + directory + ".asm"
        outputFile = open(outputFileName, 'w') # ignoring .vm
        outputFile.write(writeInit())
        outputFile.close()
        for filename in os.listdir(path):
            if filename.endswith(".vm"):
                main(path + "/" + filename, outputFileName)
    else:
        outputFileName = path[:-3] + ".asm" # ignoring .vm
        outputFile = open(outputFileName, 'w')
        outputFile.close()
        main(path, outputFileName)
