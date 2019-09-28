def main(file):
    """
        Main function which executes pass one of the assembler.
        Input: FIle name for which code needs to be translated 
        Return: None
    """
    # code for reading lines from file
    lines = [line.rstrip('\n') for line in open(file)]
    print(lines)
    for i in range(len(lines)-1,-1,-1):
        try:
            lines[i]=decode(lines[i])
        catch exception as e:
            print(e+" at line No."+str(i))

    # dir=0
    # line_counter=0
    # while dir!=2:
        
def decode(line):
    """
        Decodes a lines and extracts label, mnemonic, operands from a line
        (If there is any)
        Input : Line in a string Format
        Returns : A dictionay of label, mnemonic, operands
            1) If they are not availabe, there will be None, in place of it.
            2) operands would be a list of operands.
        # It raises the following exceptions:
        # 1) When Label format is not correct
        # 2) When the OP/CODE is not correct

    """
    l={"label":None,"mnemonic":None,"operands":[]}
    
    #remove comments from the line
    line=line[:line.index(";")]

    #check for label
    if ":" in line:
        label=line[:line.index(":")]
        l["label"]=check_label(label)
        line=line[line.index(":")+1:]
    
    opcode=""
    for i in range(len(line)):
        if line[i]==" ":
            if opcode!="":
                label["mnemonic"]=check_opcode(opcode)
                line=line[i+1:]
                break
        else:
            opcode+=line[i]

    l["operands"]=check_operands(line)    

    return l            

def check_label(label):
    """
        Check if the format of label is correct.
        Input: Label in string format
        Returns : Label in correct string format
        It raises and exception if label is not correct
        # Currently not implemented
    """
    return label.replace(" ","")

def check_opcode(opcode):
    """
        Check if the Op-Code is correct or not.
        Input: Op-code in string format.
        Returns : Interger denoting the opcode .
        Raises an exception in case of invalid op-code.
    """
    opcode=opcode.lower()
    if opcode=="CLA":
        return 1
    elif opcode=="LAC":
        return 2
    elif opcode=="SAC":
        return 3
    elif opcode=="ADD":
        return 4
    elif opcode=="SUB":
        return 5
    elif opcode=="BRZ":
        return 6
    elif opcode=="BRN":
        return 7
    elif opcode=="BRP":
        return 8
    elif opcode=="INP":
        return 9
    elif opcode=="DSP":
        return 10
    elif opcode=="MUL":
        return 11
    elif opcode=="DIV":
        return 12
    elif opcode=="STP":
        return 13
    raise Exception("Invalid OP-CODE "+opcode)
    
def check_operands(operand):
    """
        Checks for operands 
        Input : String
        Returns : list of Operands ( Empty list if it string dosen't contain any element)
        Raises Invalid Syntax Error in Operands 
        #Not implemented yet : Need to handle cases like "abc, bcd , , efg" -> abc,bcd,efg
    """

    l=[]
    for i in operand.split(","):
        l.append(i)

    return l
    

    
if __name__ == "__main__":
    main("code.txt")