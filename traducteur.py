#-*- coding: utf-8 -*-

def convertInstruction(instru):
    """ Fonction convertInstuction
    Inputs : une instruction
    ------
    Outputs : un entier représentatif de l'instruction pour notre encodage
    -------
    """ 
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
     """ Fonction getNbParameters
    Inputs : l'entier caractéristique d'une instruction
    ------
    Outputs : un entier égal au nombre de paramètres de l'instruction d'entrée
    ------- """
    if instru ==0:
            #print('Instruction stop')
            return(0)
    elif 1<=instru<=14:
            #print('Instruction à 3 paramètres : R_alpha, O, R_beta')
            return(3)
    elif 15<=instru<=17:
            #print('Instruction à 2 paramètres : r, a')
            return(2)
    elif instru==18:
            #print('Instruction à 1 paramètres : n')
            return(1)

def splitParam(registers, nb_param):
     """ Fonction splitParam
    Inputs : les registres présents en paramètres d'une instruction
    ------   le nombre de paramètres d'une instruction
    Outputs : les registres à traiter, organisés sous forme de liste
    -------
    """
    if nb_param == 1:
            n = registers.rstrip('\n')
            return(n)
    elif nb_param == 2:
            r = registers.split(',')[0] 
            a = registers.split(',')[1].rstrip('\n')
            return([r,a])
    
    elif nb_param == 3:
            R_alpha,O,R_beta = registers.rstrip('\n').split(',')
            #print(R_beta)
            #R_alpha = registers.split(',')[0] 
            #O = registers.split(',')[1] 
            #R_beta = registers.split(',')[2].rstrip('\n')
            return([R_alpha,O,R_beta])
    else:
            return([])

def convertParam(tableLabel,params,instru):
       """ Fonction convertParam
    Inputs : les paramètres d'une instruction
    ------   l'instruction associée aux paramètres
    Outputs : une liste des paramètres de l'instruction, avec la prise en compte de l'immédiat
    -------
    """
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
            elif O[0] == 'L':
                    immediat = 0
                    for l in tableLabel:
                        print("tableLabel l[0] ",l[0])#nul a refaire avec des dico
                        if O == l[0]:
                            immediat = 1
                            O = l[1]
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

def split_ligne(tableLabel,listeInstruction):
    fichier='asm.txt'
    compteur = 0
    with open(fichier, 'r') as human:
        for ligne in  human.readlines():
            #print(ligne)
            #on cherche si il y a un label
            compteur +=1
            labs = ligne.split(': ')
            if  labs[0][0]=='L':
                #il y a un label
                tableLabel.append((labs[0],compteur))
                ligne =  labs[1]
                #print(tableLabel)
             
            listeInstruction.append(ligne.strip('\n').strip('\t'))
    #return (instru,params)

def run(listeInstruction,tableLabel):

    i=0
    for i in range(len(listeInstruction)-1):#on enleve la derniere ligne
        instru, registers = listeInstruction[i].split(' ')[0], listeInstruction[i].split(' ')[1]
        
        nb_param = getNbParameters(convertInstruction(instru))
        params = splitParam(registers,nb_param)
        print("parametre ",nb_param)
        cvted_inst = [convertInstruction(instru)]
        cvted_param = convertParam(tableLabel,params,instru)
        cvted_all = cvted_inst+cvted_param
        
        print("table de label:",tableLabel)
        print("conversion de l'instruction:",cvted_all)

        listToBin(cvted_all,nb_param,instru)            

def listToBin(l,params,instru):
    """ Fonction listToBin : Cette fonction écrit en binaire dans un fichier bin.txt les instructions issues de asm.txt une fois encodée 
    Inputs : une liste contenant les informations encodées d'une instruction
    ------   un entier donnant le nombre de paramètres de l'instruction
    Outputs : Aucune
    ------- 
    """
    
    l = [int(i) for i in l]
    binaire = 0
    binaire+=l[0]<<27

    if(params == 3):
        binaire+=l[1]<<22
        binaire+=l[2]<<21
        binaire+=l[3]<<5
        binaire+=l[4]
        
    elif(params == 2):
        if(instru == 'JMP'):
            binaire+=l[1]<<26
            binaire+=l[2]<<5
            binaire+=l[3]
        else:
            binaire+=l[1]<<22
            binaire+=l[2]

    elif(params == 1):
        binaire+=l[1]
    else:
        print("aucun param")
    hexa=hex(binaire)
    hexa+='\n'
    print(hexa)
                    
    with open('bin.txt', 'a') as output:
        output.write(hexa)
    #print(tableLabel[i][0])
        
def main():
        """ Fonction main : boucle d'exécution principale """
    
    with open('bin.txt', 'w') as output:
        output.write('')
    tableLabel = [] 
    listeInstruction = []
    split_ligne(tableLabel,listeInstruction)
    run(listeInstruction,tableLabel)



if __name__ == '__main__':
    main()
