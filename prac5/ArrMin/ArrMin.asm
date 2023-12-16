// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// Initialize c to 1
@c
M=1            

// Load the value at R1 into D
@R1
A=M
D=M             

// Store the value from D into R0
@R0
M=D             

// Increment the value at R1
@R1
M=M+1           

(LOOP)
@R2
D=M

// Calculate the difference between R2 and c
@c
D=D-M           

// Check if the difference is 0 (equal)
@END
D;JEQ            

@R0
D=M

// Check if D is negative
@NEGATIVE
D;JLT              

(POSITIVE)
@R1
A=M
D=M

// Check if D is positive or negative
@POSITIVEORNEGATIVE
D;JLT              

@R0
D=M
    
@R1
A=M
D=D-M

// Check if D is greater than 0
@NEW
D;JGT                 

// If none of the above, increment and jump to INCREMENT
@INCREMENT
0;JMP                 

(POSITIVEORNEGATIVE)
@R1
A=M
D=M

// Store D into R0
@R0
M=D              

// Jump to INCREMENT
@INCREMENT
0;JMP            

(NEGATIVE)
@R1
A=M
D=M

// If D is negative, increment and jump to INCREMENT
@INCREMENT
D;JGT               

@R0
D=M
   
@R1
A=M
D=M-D

// Check if D is less than 0
@NEW
D;JLT              

@INCREMENT
0;JMP

(NEW)
@R1
A=M
D=M

// Store D into R0
@R0
M=D                     

(INCREMENT)
@R1
M=M+1

@c
M=M+1

// Jump back to LOOP
@LOOP
0;JMP                   

(END)
@END
0;JMP
