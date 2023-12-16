// Sorts the array of length R2 whose first element is at RAM[R1] in ascending order in place. Sets R0 to True (-1) when complete.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Initialize variables
@R1      // Address of the first element in R1
D=M      // D = first element
@R2
M=M-1    // Decrement the length counter in R2
D=M      // D = LENGTH
@LENGTH
M=D      // Store LENGTH in LENGTH

(FIRST)
@R1      // Load address of the first element in R1
A=M

(SECOND)
@R1      // Load address of the first element in R1
A=M
D=M      // D = current element
A=A+1
D=M-D    // D = next element - current element

// Check if D >= 0 (current <= next)
@POSITIVE
D;JGE

// Swap current and next elements
@R1
A=M
D=M
@TEMP
M=D      // Store the current element in TEMP
@R1
A=M+1
D=M
@R1
A=M
M=D      // Set the current element to the next element
@TEMP
D=M      // Load the current element from TEMP
@R1
A=M+1
M=D      // Set the next element to the current element from TEMP

// Increment the current index in R1
(POSITIVE)
@R1
M=M+1

// Decrement the length in LENGTH
@LENGTH
M=M-1
D=M

// Jump to SECOND if D is greater than 0
@SECOND
D;JGT

// Increment the current index in R1
@R1
M=M+1

// Decrement the length counter in R2
@R2
M=M-1
D=M

// Jump to FIRST if D is greater than 0
@FIRST
D;JGT

// Jump to END_LOOP if D is equal to 0
@END_LOOP
D;JEQ

// Set R0 to -1 to indicate completion
(END_LOOP)
@R0
M=-1

// Jump to END to finish the program
(END)
@END
0;JMP
