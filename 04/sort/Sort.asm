//
// This piece of code sorts the array which starts at the address in R14
// of length that is in R15. It sorts in descending order, using Bubble Sort.
// https://en.wikipedia.org/wiki/Bubble_sort
//


@R14
D=M
@outterInd
M=D
(OUTTERLOOP)



@innerInd




(SWAP) // swaps @firstAdr with @secondAdr
    @firstAdr // get first address 
    A=M
    D=M
    @firstVal // save value of first adr
    M=D
    @secondAdr // get second adr
    A=M
    D=M
    @firstAdr // set value of first adr
    A=M
    M=D
    @firstVal // get value of first var
    D=M
    @secondAdr // set valur of second adr
    A=M
    M=D
    @innerInd
    D=M
    
    @INNERLOOP
    0;JMP
(END)
