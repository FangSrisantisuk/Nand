// Calculates R1 + R2 - R3 and stores the result in R0.
// (R0, R1, R2, R3 refer to RAM[0], RAM[1], RAM[2], and RAM[3], respectively.)

// Put your code here.
@R1 // Load a into A register
D=M // D = a

@R2 // Load b into A register
D=D+M // D = a + b

@R3 // Load c into A register
D=D-M // D = (a+b) - c

@R0 // Store the result in R0
M=D
0;JMP