'''
TODO:
    Add the word 'Exception'
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
success = True


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
    global success

    instructions = {}
    symbol_table = {}
    location_counter = 0

    with open('code.txt') as file:
        for line in file:

            line = line.strip()
            if line == '':
                continue

            instruction = get_instruction(line)
            instructions[instruction['location']] = instruction

    check_symbol_table()
    check_for_stop()

    temp_file = {'instructions': instructions, 'symbol_table': symbol_table, 'success': success}
    
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
    instruction['location'] = location_counter
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
    assign_operands(instruction)

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

    if address == None:
        if label in symbol_table:
            return
        else:
            symbol_table[label] = None
            return

    if label in symbol_table and symbol_table[label] != None and address != None:
        print(instructions)
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
    
def assign_operands(instruction):
    """
        Checks for operands 
        Input : 
        Returns : list of Operands ( Empty list if it string dosen't contain any element)
        Raises Invalid Syntax Error in Operands 
        #Not implemented yet : Need to handle cases like "abc, bcd , , efg" -> abc,bcd,efg
    """

    if len(instruction["operands"]) != instruction["opcode"]["NUMBER OF OPERANDS"]:
        raise Exception("Opcode supplied with wrong number of operands")
    
    if instruction["opcode"]["TYPE OF OPERAND"] == "LABEL":
        put_in_symbol_table(instruction['operands'][0], None)
 
def check_symbol_table():
    for symbol in symbol_table:
        if symbol_table[symbol] == None:
            raise Exception(symbol + " not defined")
    return True

def check_for_stop():
    global location_counter
    global instructions

    if instructions[location_counter - 1] != 'STP':
        raise Exception("STP Missing at end of code")

def createJSON(nameOfFile, dict_data):
    with open(nameOfFile+'.json', 'w') as json_file:
        json.dump(dict_data, json_file)


first_pass('code.txt')