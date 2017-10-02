// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(CLEAR)
// Init loop
    @SCREEN
    D=A
    @i
    M=D
(CLEARLOOP)
    @i
    A=M
    M=0
// next pixel
    @i
    M=M+1
// save it for compare
    D=M
// reached KBD address, end of screen.
    @KBD
    D=D-A
    @CLEARLOOP
    D;JNE

(STAYCLEAR)
    @KBD
    D=M
    @STAYCLEAR
    D;JEQ

(BLACK)
// Init loop
    @SCREEN
    D=A
    @i
    M=D
(BLACKLOOP)
    @i
    A=M
    M=-1
// next pixel
    @i
    M=M+1
// save it for compare
    D=M
// reached KBD address, end of screen.
    @KBD
    D=D-A
    @BLACKLOOP
    D;JNE
(STAYBLACK)
    @KBD
    D=M
    @STAYBLACK
    D;JGT

    @CLEAR
    0;JMP
(END)
    @END
    0;JMP
