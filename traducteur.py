#-*- coding: utf-8 -*-

def convertInstruction(instru):
    instru = instru.upper()
    if instru=='ADD':
            return(1)
    elif instru=='SUB':
            return(2)
    elif instru=='MULT':
            return(3)
    elif instru=='DIV':
            return(4)
    elif instru=='AND':
            return(5)
    elif instru=='OR':
            return(6)
    elif instru=='XOR':
            return(7)
    elif instru=='SHL':
            return(8)
    elif instru=='SHR':
            return(9)
    elif instru=='SLT':
            return(10)
    elif instru=='SLE':
            return(11)
    elif instru=='SEQ':
            return(12)
    elif instru=='LOAD':
            return(13)
    elif instru=='STORE':
            return(14)
    elif instru=='JMP':
            return(15)
    elif instru=='BRAZ':
            return(16)
    elif instru=='BRANZ':
            return(17)
    elif instru=='SCALL':
            return(18)
    elif instru=='STOP':
            return(0)
    else:
            return('Error while reading the instruction')

def getNbParameters(instru):
    if instru ==0:
            print('Instruction stop')
            return(0)
    elif 1<=instru<=14:
            print('Instruction à 3 paramètres : R_alpha, O, R_beta')
            return(3)
    elif 15<=instru<=17:
            print('Instruction à 2 paramètres : r, a')
            return(2)
    elif instru==18:
            print('Instruction à 1 paramètres : n')
            return(1)

def splitParam(registers, nb_param):
    if nb_param == 1:
            n = registers.rstrip('\n')
            return(n)
    elif nb_param == 2:
            r = registers.split(',')[0] 
            a = registers.split(',')[1].rstrip('\n')
            return([r,a])
    
    elif nb_param == 3:
            R_alpha,O,R_beta = registers.rstrip('\n').split(',')
            print(R_beta)
            #R_alpha = registers.split(',')[0] 
            #O = registers.split(',')[1] 
            #R_beta = registers.split(',')[2].rstrip('\n')
            return([R_alpha,O,R_beta])
    else:
            return([])

def convertParam(params,instru):
    n = len(params)
    if n==3:
            R_alpha=params[0][1:]
            R_beta=params[2][1:]
            O=params[1]
            if O[0]=='R':
                    immediat=0
                    O=O[1:]
            else:
                    immediat=1
            conversion=[R_alpha,immediat,O,R_beta]
    elif n ==2:
        if instru == 'JMP':
            O = params[0]
            r = params[1][1:]

            if O[0]=='R':
                    immediat=0
                    O=O[1:]
            else:
                    immediat=1
            conversion=[immediat,O,r]
        else:
            r = params[0][1:]
            a = params[1][1:]
            conversion = [r,a]
    elif n ==1:
        n = params[0][1:]
    else:
            conversion = []
    return (conversion)

def split_ligne(tableLabel,compteur):
    fichier='asm.txt'
    
    with open(fichier, 'r') as human:
            ligne = human.readline()
            print(ligne)
            #on cherche si il y a un label
            labs = ligne.split(': ')
            if  labs[0][0]=='L':
                #il y a un label
                tableLabel.append((labs[0],compteur))
                print("label enregistré",labs)
                print("==========================")
                ligne =  labs[1]
                print(tableLabel)
                print("ligne sans label\n")
                print(ligne)

            instru, registers = ligne.split(' ')[0], ligne.split(' ')[1]
            nb_param = getNbParameters(convertInstruction(instru))
            params = splitParam(registers,nb_param)

    return(instru,params)

def listToBin(l,params):
    l = [int(i) for i in l]
    binaire = 0
    binaire+=l[0]<<27
    if(params == 3):
        binaire+=l[1]<<22
        binaire+=l[2]<<21
        binaire+=l[3]<<5
        binaire+=l[4]
        hexa=hex(binaire)
        hexa+='\n'
        with open('bin.txt', 'w') as output:
                output.write(hexa)
        
    elif(params == 2):
        if(instru == 'JMP'):
            binaire+=l[1]<<26
            binaire+=l[2]<<5
            binaire+=l[3]
            hexa=hex(binaire)
            hexa+='\n'
            with open('bin.txt', 'w') as output:
                output.write(hexa)
        else:
            binaire+=l[1]<<22
            binaire+=l[2]
            hexa=hex(binaire)
            hexa+='\n'
            with open('bin.txt', 'w') as output:
                output.write(hexa)

    elif(params == 1):
        binaire+=l[1]
        hexa=hex(binaire)
        hexa+='\n'
        with open('bin.txt', 'w') as output: 
            output.write(hexa)

    else:
        hexa=hex(binaire)
        hexa+='\n'
        with open('bin.txt', 'w') as output:
            output.write(hexa)
                    
            #print(tableLabel[i][0])
        
def main():
    #tableLabel = label()
    #remplaceLabel(tableLabel)

    tableLabel = []    
    instru, params = split_ligne(tableLabel,1)
    cvted_inst = [convertInstruction(instru)]
    cvted_param = convertParam(params,instru)
    cvted_all = cvted_inst+cvted_param
    print(cvted_all)   
    listToBin(cvted_all,params)            

if __name__ == '__main__':
    main()
