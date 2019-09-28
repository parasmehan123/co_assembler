'''
TODO:
    assign_operand {check with opcode[number of operands], if type of operands is symbol, insert in symbol table}
    check_symbol_table

'''

import json

opcodes = {
    'CLA': {
        'CODE': '0000', 
        'NUMBER OF OPERANDS': 0,
        'TYPE OF OPERAND': None,
        'OUTPUT': []
    },
    'LAC': {
        'CODE': '0001', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'ADDRESS',
    },
    'SAC': {
        'CODE': '0010', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'ADDRESS',
    },
    'ADD': {
        'CODE': '0011', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'ADDRESS'
    },
    'SUB': {
        'CODE': '0100', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'ADDRESS'
    },
    'BRZ': {
        'CODE': '0101', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'LABEL'
    },
    'BRN': {
        'CODE': '0110', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'LABEL'
    },
    'BRP': {
        'CODE': '0111', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'LABEL'
    },
    'INP': {
        'CODE': '1000', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'ADDRESS'
    },
    'DSP': {
        'CODE': '1001', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'ADDRESS'
    },
    'MUL': {
        'CODE': '1010', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'ADDRESS'
    },
    'DIV': {
        'CODE': '1011', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'ADDRESS'
    },
    'STP': {
        'CODE': '1100', 
        'NUMBER OF OPERANDS': 0,
        'TYPE OF OPERAND': None
    }
}

instructions = {}
symbol_table = {}
location_counter = 0
has_successfully_compiled = True


def first_pass(file):
    """
        Main function which executes pass one of the assembler.
        Input: FIle name for which code needs to be translated 
        Return: None
    """
    # code for reading lines from file
    global temp_file
    global instructions
    global symbol_table
    global location_counter
    global has_successfully_compiled

    instructions = {}
    symbol_table = {}
    location_counter = 0
    success = True


    with open('code.txt') as file:
        for line in file:

            line = line.strip()
            if line == '':
                continue

            instruction = get_instruction(line)
            instructions[instruction['location']] = instruction
            # except Exception as e:
            #     print('Exception at line ' + str(location_counter))
            #     print(e)
            #     success = False

    success = success and check_symbol_table()

    temp_file = {'instructions': instructions, 'symbol_table': symbol_table, 'has_successfully_compiled': success}
    
    createJSON('temp_file', temp_file)
    return success

def get_instruction(line):
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

    global location_counter

    instruction = {
        "location": None, 
        "label": None, 
        "mnemonic": None, 
        'opcode' : None,
        "operands": None, 
        "comment": None
    }

    # Check for comment and remove from line
    if ';' in line:
        line, comment = line.split(';')
        instruction['comment'] = comment



    # Assign address to instruction and increment location counter
    instruction['location'] = '0' * (8 - len(bin(location_counter)[2:])) + bin(location_counter)[2:]
    location_counter += 1

    # Check for label and insert in symbol table if exists
    if ":" in line:
        label, line = line.split(': ', 1)
        instruction["label"] = label
        put_in_symbol_table(label, instruction['location'])
    
    # Split line into opcode and operands
    words = list(line.split())
    instruction['mnemonic'] = words[0]
    instruction['operands'] = words[1:]

    # Look up mnemonic in opcode table and assign information about the opcode
    assign_opcode(instruction)

    return instruction

def put_in_symbol_table(label, address):
    """
        Check if the format of label is correct.
        Input: Label in string format
        Returns : Label in correct string format
        It raises and exception if label is not correct
        # Currently not implemented
    """
    global symbol_table

    if label != None:
        if label in symbol_table and symbol_table[label] != None:
            raise Exception('Exception: ' + label + ' declared multiple times')
        else:
            symbol_table[label] = address
    
def assign_opcode(instruction):
    """
        Assign Opcode if it is a valid opcode
        Input: Opcode in string format.
        Returns : None
        Raises an exception in case of invalid opcode.
    """
    opcode = instruction['mnemonic']
    if opcode in opcodes:
        instruction['opcode'] = opcodes[opcode]
    else:
        raise Exception(opcode + ' not a valid opcode')
    
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

def check_symbol_table():
    for symbol in symbol_table:
        if symbol_table[symbol] == None:
            return False
    return True

def createJSON(nameOfFile, dict_data):
    with open(nameOfFile+'.json', 'w') as json_file:
        json.dump(dict_data, json_file)


first_pass('code.txt')