//
// This piece of code sorts the array which starts at the address in R14
// of length that is in R15. It sorts in descending order, using Bubble Sort.
// https://en.wikipedia.org/wiki/Bubble_sort
//


@outerCount
M=0

(OUTTERLOOP)
    @R15
    D=M
    @outerCount  // goes from 0 to R15
    M=M+1
    D=D-M
    @END
    D;JEQ
    @innerCount
    M=1

(INNERLOOP)
    @R15
    D=M
    @innerCount
    M=M+1
    D=D-M
    @OUTTERLOOP
    D;JLT
    @R14
    A=D+M // first address
    D=A // save first address
    @firstAdr
    M=D
    A=M // back to place
    D=M // save value
    A=A+1
    D=D-M
    @INNERLOOP
    D;JGT

(SWAP) // swaps @firstAdr with @secondAdr
    @firstAdr // get first address 
    A=M
    D=M
    @firstVal // save value of first adr
    M=D
    @firstAdr // get second adr
    A=M+1
    D=M
    @firstAdr // set value of first adr
    A=M
    M=D
    @firstVal // get value of first var
    D=M
    @firstAdr // set valur of second adr
    A=M+1
    M=D
    @innerInd
    D=M
    
    @INNERLOOP
    0;JMP
(END)
