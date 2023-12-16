// This file is based on part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: Mult.asm

// Multiplies R1 and R2 and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

(LOOP)
@R0
M=0

// Load the value at R1 into D
@R1
D=M         
@NEGATIVE
D;JLT
@LOOP
0;JMP

(NEGATIVE)

// Negate the value in R1
@R1
M=-M        
// Negate the value in R2   
@R2
M=-M          

(LOOP)
// Load the value at R1 into D
@R1
D=M           
// If R1 is zero, jump to END_LOOP
@END
D; JEQ        

// Load the value at R0 into D
@R0
D=M            
// Add the value in R2 to D
@R2
D=D+M          
// Store the result back in R0
@R0
M=D            

// Decrement the value in R1
@R1
M=M-1   
// Jump back to LOOP       
@LOOP
0; JMP        

(END)
