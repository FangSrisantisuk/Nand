class VMTranslator:
    jump = {"eq":0, "gt": 0, "lt": 0}
    segments = {'local':"LCL",
                'argument':"ARG",
                'this':"THIS",
                'that':"THAT"
                }
    call_counter = 0
    
    @classmethod 
    def vm_init(cls):
        lines = []
        lines.extend(["@256",
            "D=A",
            "@SP",
            "M=D",
            "@300",
            "D=A",
            "@LCL",
            "M=D",
            "@400",
            "D=A",
            "@ARG",
            "M=D",
            "@3000",
            "D=A",
            "@THIS",
            "M=D",
            "@3010",
            "D=A",
            "@THAT",
            "M=D"])
        return "\n".join(lines)

    @classmethod 
    def vm_push(cls, segment, offset):
        '''Generate Hack Assembly code for a VM push operation'''
        lines = []
        if segment in cls.segments:
            if offset == 0: 
                lines.extend([
                    f"@{cls.segments[segment]}",
                    "A=M"
                ])
            if offset > 0 and offset < 3:
                lines.extend([
                    f"@{cls.segments[segment]}",
                    "A=M+1"
                ])
                for _ in range(offset-1):
                    lines.extend(["A=A+1"])
            else:
                lines.extend([
                    f"@{cls.segments[segment]}",
                    "D=M",
                    f"@{offset}",
                    "A=D+A"
                ])   
            lines.extend(["D=M"])  
        elif segment == 'temp':
            address = offset + 5
            lines.extend([
                f"@{address}",
                "D=M"
            ])
        elif segment == 'constant':
            address = offset 
            lines.extend([
                f"@{address}",
                "D=A"
            ])
        elif segment == 'pointer':
            if offset == 0:
                address = "THIS"
            elif offset == 1:
                address = "THAT"
            else:
                raise ValueError(f"Invalid pointer {offset}")
            lines.extend([
                f"@{address}",
                "D=M"
            ])
        elif segment == 'static':
            lines.extend([
                f"@{16 + offset}",
                "D=M"
            ])
        lines.extend([
            "@SP",
            "AM=M+1",
            "A=A-1",
            "M=D"
        ])
        return '\n'.join(lines)

    @classmethod
    def vm_pop(cls,segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        lines = []
        lines.extend([
                "@SP",
                "AM=M-1",
                "D=M"
            ])
        if segment in cls.segments:
            if offset == 0:
                lines.extend([
                    f"@{cls.segments[segment]}",
                    "A=M"
                ])
            if offset > 0: 
                lines.extend([
                    f"@{cls.segments[segment]}",
                    "A=M+1"
                ])
                for _ in range(offset-1):
                    lines.extend(["A=A+1"])
        elif segment == 'temp':
            address = offset + 5
            lines.extend([f"@{address}"])
        elif segment == 'pointer':
            if offset == 0:
                address = "THIS" 
            elif offset == 1:
                address = "THAT"
            else:
                raise ValueError(f"Invalid pointer {offset}")
            lines.extend([f"@{address}"])
        elif segment == 'static':
            lines.extend([f"@{16+offset}"])
        lines.extend(["M=D"])
        return '\n'.join(lines)

    @staticmethod 
    def loadBinary():
        lines = []
        lines.extend(["@SP",
            "AM=M-1",
            "D=M",
            "A=A-1"])
        return lines 

    @staticmethod
    def loadUnary():
        lines = []
        lines.extend(["@SP",
            "A=M-1"])
        return lines 

    @classmethod
    def vm_add(cls):
        '''Generate Hack Assembly code for a VM add operation'''
        lines = cls.loadBinary()
        lines.extend(["M=D+M"])
        return '\n'.join(lines)

    @classmethod
    def vm_sub(cls):
        '''Generate Hack Assembly code for a VM sub operation'''
        lines = cls.loadBinary()
        lines.extend(["M=M-D"])
        return '\n'.join(lines)

    @classmethod
    def vm_neg(cls):
        '''Generate Hack Assembly code for a VM neg operation'''
        lines = cls.loadUnary()
        lines.extend(["D=!M"])
        lines.extend(["M=D+1"])
        return '\n'.join(lines)

    @classmethod 
    def vm_eq(cls):
        '''Generate Hack Assembly code for a VM eq operation'''
        lines = []
        lines.extend(["@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "D=M-D",
            "M=0",
            f"@END_EQ_{cls.jump['eq']}",
            f"D;JNE",
            "@SP",
            "A=M-1",
            "M=-1",
            f"(END_EQ_{cls.jump['eq']})"])
        cls.jump['eq'] += 1
        return '\n'.join(lines)

    @classmethod  
    def vm_gt(cls):
        '''Generate Hack Assembly code for a VM gt operation'''
        lines = []
        lines.extend(["@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "D=M-D",
            "M=0",
            f"@END_GT_{cls.jump['gt']}",
            f"D;JLE",
            "@SP",
            "A=M-1",
            "M=-1",
            f"(END_GT_{cls.jump['gt']})"])
        cls.jump['gt'] += 1
        return '\n'.join(lines)

    @classmethod
    def vm_lt(cls):
        '''Generate Hack Assembly code for a VM lt operation'''
        lines = []
        lines.extend(["@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "D=M-D",
            "M=0",
            f"@END_LT_{cls.jump['lt']}",
            f"D;JGE",
            "@SP",
            "A=M-1",
            "M=-1",
            f"(END_LT_{cls.jump['lt']})"])
        cls.jump['lt'] += 1
        return '\n'.join(lines)

    @classmethod 
    def vm_and(cls):
        '''Generate Hack Assembly code for a VM and operation'''
        lines = cls.loadBinary()
        lines.extend(["M=D&M"])
        return '\n'.join(lines)

    @classmethod 
    def vm_or(cls):
        '''Generate Hack Assembly code for a VM or operation'''
        lines = cls.loadBinary()
        lines.extend(["M=D|M"])
        return '\n'.join(lines)

    @classmethod
    def vm_not(cls):
        '''Generate Hack Assembly code for a VM not operation'''
        lines = cls.loadUnary()
        lines.extend(["M=!M"])
        return '\n'.join(lines)

    @classmethod
    def vm_label(cls, label):
        '''Generate Hack Assembly code for a VM label operation'''
        return f"({label})"

    @classmethod
    def vm_goto(cls,label):
        '''Generate Hack Assembly code for a VM goto operation'''
        lines = []
        lines.extend([f"@{label}",
            "0;JMP"])
        return '\n'.join(lines)

    @classmethod
    def vm_if(cls,label):
        '''Generate Hack Assembly code for a VM if-goto operation'''
        lines = []
        lines.extend(["@SP",
            "AM=M-1",
            "D=M",
            f"@{label}",
            f"D;JNE"])
        return '\n'.join(lines)
        
    @classmethod
    def vm_function(cls, function_name, n_vars):
        '''Generate Hack Assembly code for a VM function operation'''
        lines = []
        lines.extend([f"({function_name})"])
        if n_vars > 0: 
            lines.extend([f"@{n_vars + 1}",
                "D=A",
                f"(LOOP_{function_name})",
                "D=D-1",
                "@SP",
                "AM=M+1",
                "A=A-1",
                "M=0",
                f"@LOOP_{function_name}",
                "D;JGT"])
        return '\n'.join(lines)

    @classmethod
    def vm_call(cls,function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        lines = []
        lines.extend([
            f"@{n_args}",
            "D=A",
            "@R13",
            "M=D",

            f"@{function_name}",
            "D=A",
            "@R14",
            "M=D",

            f"@RET_ADDRESS_CALL_{cls.call_counter}",
            "D=A",
            "@SP",
            "A=M",
            "M=D",

            "@LCL",
            "D=M",
            "@SP",
            "AM=M+1",
            "M=D",

            "@ARG",
            "D=M",
            "@SP",
            "AM=M+1",
            "M=D",

            "@THIS",
            "D=M",
            "@SP",
            "AM=M+1",
            "M=D",

            "@THAT",
            "D=M",
            "@SP",
            "AM=M+1",
            "M=D",

            "@4",
            "D=A",
            "@R13", 
            "D=D+M",
            "@SP",
            "D=M-D",
            "@ARG",

            "M=D",
            "@SP",
            "MD=M+1",
            "@LCL",
            "M=D",
            "@R14",
            "A=M",
            "0;JMP",
            f"(RET_ADDRESS_CALL_{cls.call_counter})"
        ])
        
        cls.call_counter +=1 
        return '\n'.join(lines)

    @classmethod
    def vm_return(cls):
        '''Generate Hack Assembly code for a VM return operation'''
        lines = []
        lines.extend([
            "@5",      # Load 5 into D
            "D=A",
            "@LCL",    # Load the base address of the current LCL frame into A
            "A=M-D",   # Calculate the target address (LCL - 5) and load it into A
            "D=M",     # Load the value at the target address into D
            "@R13",    # Store D in R13
            "M=D",

            "@SP",     # Load the stack pointer address into A
            "AM=M-1",  # Decrement the stack pointer
            "D=M",     # Load the value on top of the stack into D
            "@ARG",    # Load the base address of the current ARG segment into A
            "A=M",     # Load the target address (ARG) into A
            "M=D",     # Store the value from D at the target address

            "D=A",     # Load the value in ARG into D
            "@SP",     # Load the stack pointer address into A
            "M=D+1",   # Set SP to ARG + 1
            "@LCL",    # Load the base address of the current LCL frame into A
            "D=M",     # Load the value at A (LCL base) into D
            "@R14",    # Store D in R14
            "AM=D-1",  # Load the value at (LCL-1) into A and D
            "D=M",     # Load the value in D
            "@THAT",   # Load the address of THAT into A
            "M=D",     # Store D in THAT
    
        # Repeat the same pattern for THIS, ARG, and LCL
            "@R14",
            "AM=M-1",
            "D=M",
            "@THIS",
            "M=D",

            "@R14",
            "AM=M-1",
            "D=M",
            "@ARG",
            "M=D",
            
            "@R14",
            "AM=M-1",
            "D=M",
            "@LCL",
            "M=D",
    
        # Jump to the return address stored in R13
            "@R13",
            "A=M",
            "0;JMP"    # Unconditional jump
        ])
        return '\n'.join(lines)

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):        
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))