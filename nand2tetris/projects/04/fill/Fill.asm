// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.


(LOOP)
	@24576
	D = M 
	@key
	M = D //key represents the latest character pressed
	
	@BLACK // if key > 0, jump to the black loop
	D; JGT
	
	@WHITE
	D; JMP // creates the infinite loop
			
(END)
	
(BLACK)

	@8192
	M = A
	@i
	D = M
	@i
	M = D
	(INNER)
		@65535
		D = A
		@val
		M = D
		
		@i
		D = M
		@i
		M = D
		
		@16384
		A = A + 1
		M = D
		
		@i
		D = M - 1
		@i
		M = D
		@INNER
		D;JGT
		
	@LOOP
	0;JMP
	
(WHITE)

	@8192
	M = A
	@i
	D = M
	@i
	M = D
	@16384
	D = A
	@16384
	M = D
	
	(WINNER)
		@65535
		D = A
		@val
		M = D
		
		@i
		D = M
		@i
		M = D
		@16384
		A = A + 1
		M = D
		
		@i
		D = M - 1
		@i
		M = D
		@WINNER
		D;JGT
		
	@LOOP
	0;JMP