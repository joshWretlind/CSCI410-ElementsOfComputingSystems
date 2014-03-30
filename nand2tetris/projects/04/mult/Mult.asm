// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

// Put your code here.

@R0
D = M
@x
M = D // X=R0

@1
D = M
@y
M = D // y=R1

@mult
M = 0 //mult= 0

(WHILE)
	@y
	D = M // D=y
	
	@END
	D;JLE //End if D <=0
	
	@x
	D = M //Load x into D
	
	@mult
	M = D + M //
	@mult
	D = M
	@R2
	M = D
	
	@1
	D = A
	@y
	M = M - D
	@WHILE
	0;JMP
(END)
	@END
	0;JMP