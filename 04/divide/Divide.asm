// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/divide/Divide.asm

// The program should divide two numbers - R13 / R14 and put the 
// result in R15.
	
	@R15    // target
	M=0  	// starts at 0

	@R14
	D=M
	@END
	D;JEQ   // Can't divide by zero

	@divider
	M=D     // divider = R14
	
	@R13    // number
	D=M
	@remainder
	M=D     // remainder = R13
	
	@muler
	M=1     // init muler with 1
	
(WHILE)
	@R13 
	D=M
	@divider
	D=M-D   
	@FIRSTACTION
	D;JGE   // if (divider - R13) >= 0 jmp FIRSTACTION
	
	@divider
	M=M<<   // divider divided by two
	@muler
	M=M<<   // multiplier divided by two
	@WHILE
	0;JMP   // repeat while loop

(FIRSTACTION)
	@divider
	D=M
	@remainder
	D=M-D
	@SECONDACTION
	D;JLT  // if (remainder - divider) < 0 jmp SECONDACTION
	
	@divider
	D=M
	@remainder
	M=M-D  // remainder = remainder - divider
	
	@muler
	D=M
	@R15
	M=D+M  // target = target + muler
	
(SECONDACTION)
	@divider
	M=M>>   // divider /= 2
	@muler
	M=M>>   // muler /= 2
	@muler
	D=M
	@FIRSTACTION
	D;JNE  // if (muler != 0) jmp FIRSTACTION

(END)
