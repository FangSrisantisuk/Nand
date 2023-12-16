// Calculates the absolute value of R1 and stores the result in R0.
// (R0, R1 refer to RAM[0], and RAM[1], respectively.)

// Put your code here.

@R1 // Load the number into the A register
D=M // D = number

// Check if D (number) is negative
@NEGATIVE
D;JLT // Jump to NEGATIVE if D is less than 0 (negative)

// If D is not negative, it's already the absolute value
@END
0;JMP

(NEGATIVE)
// Negate D (number) to get the absolute value
D=-D // D = -number

(END)
@R0 // Store the result in R0
M=D

// Infinite loop to halt the program
@END
0;JMP