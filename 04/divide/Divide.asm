// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/divide/Divide.asm

// The program should divide two numbers - R13 / R14 and put the 
// result in R15.
	
	@R15
	M=0  	// init R15 == 0
	

	@R14
	D=M
	@END
	D;JEQ   // if (R14 == 0) goto END

	@R14
	D=M
	@divisor
	M=D     // divisor = R14
	
	@R13
	D=M
	@remain
	M=D     // remain = R13
	
	@1 
	D=A
	@mul
	M=D     // init mul ==1
	
(WHILE)
	@R13
	D=M
	@divisor
	D=M-D   
	@DO
	D;JGE   // if (divisor - R13) >= 0 goto DO
	
	@divisor
	M=M<<   // divisor =* 2
	@mul
	M=M<<   // mul =* 2
	@WHILE
	0;JMP   // repeat while loop

(DO)
	@divisor
	D=M
	@remain
	D=M-D
	@ELSE
	D;JLT  // if (remain - divisor) < 0 goto ELSE
	
	@divisor
	D=M
	@remain
	M=M-D  // remain = remain - divisor
	
	@mul
	D=M
	@R15
	M=D+M  // res = res + mul
	
(ELSE)
	@divisor
	M=M>>   // divisor /= 2
	@mul
	M=M>>   // mul /= 2
	
	@mul
	D=M
	@DO
	D;JNE  // if (mul != 0) goto DO

(END)
