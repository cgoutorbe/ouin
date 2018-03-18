programs = []
regs = []
pc = 0
memInstr = []
memData = []

fonction = {}

fonction[1] = "ADD"
fonction[2] = "SUB" 
fonction[3] = "MULT"
fonction[4] = "DIV"
fonction[5] = "AND"
fonction[6] = "OR"
fonction[7] = "XOR"
fonction[8] = "SHL"
fonction[9] = "SHR"
fonction[10] = "SLT"
fonction[11] = "SLE"
fonction[12] = "SEQ"
fonction[13] = "LOAD"
fonction[14] = "STORE"
fonction[15] = "JMP"
fonction[16] = "BRAZ"
fonction[17] = "BRANZ"
fonction[18] = "SCALL"
fonction[0] = "STOP"

def binToInstr(instr):
    """ Fonction binToInstr
    Inputs : une instruction
    ------
    Outputs : un entier correspondant au code d'instruction 
    """
    return (int((instr & 0xF8000000)>>27))

def decode(instr,i):
    """ Fonction decode
    Inputs : une instruction 
    ------   un entier correspondant au code de l'instruction traitée
    Output : une liste comprenant le décodage de l'information selon la norme définie en cours
    ------
    """ 
    
    if 1<i<14:
        codeop = (instr & 0xF8000000) >> 27
        r_alpha = (instr & 0x07C00000) >> 22
        imm = (instr & 0x00200000) >> 21
        O = (instr & 0x001FFFE0) >> 5
        r_beta = (instr & 0x000001F)
        return([codeop,r_alpha,imm,O,r_beta])

    elif i == 0:
        codeop = (instr & 0xF8000000) >> 27
        return([codeop])
    elif i == 15:
        codeop = (instr & 0xF8000000) >> 27
        imm = (instr & 0x04000000) >> 26
        O = (instr & 0x03FFFFE0) >> 5
        r = (instr & 0x00000F)
        return([codeop,imm,O,r])

    elif 15<i<17:
        codeop = (instr & 0xF8000000) >> 27
        r = (instr & 0x07C00000) >> 22
        a = (instr & 0x003FFFFF)
        return([codeop,r,a])
    else:
        codeop = (instr & 0xF8000000) >> 27
        n = (instr & 0x07FFFFFF)
        return([codeop,n])

def run(instruction):
    
    i = binToInstr(instruction)
    memInstr.append(decode(instruction,i))
    print(memInstr)
    #appel de la fonction correspondant à l'instruction
    


def main():
    """ Fonction main : Boucle d'execution principale """  
    
    global pc
    pc=0
    
    with open('bin.txt', 'r') as f:
        lines = f.readlines()
        print(lines)
    
    for line in lines:
        print(line)
        run(int(line,16))
        pc+=1



if __name__ == '__main__':
    main()
