programs = []
regs = []
pc = 0

def fetch(fichier):
    with open(fichier, 'r') as f:
            global pc
            pc += 1
            line = f.readline()
            print(line)
    return(line)
# A Regrouper

def binToInstr(instr):
    return (int((instr & 0xF8000000)>>27))


def decode(instr,i):
    
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

def main():
    
    pc=0
    instruction = int(fetch('bin.txt'),16)
    i = binToInstr(instruction)
    print(decode(instruction,i))
    



if __name__ == '__main__':
    main()
