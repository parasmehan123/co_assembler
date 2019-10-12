'''
TODO:
    Add the word 'Exception'
'''


'''
Osheens-MacBook-Air-1115:co_assembler osheensachdev$ python3 Main.py 
list index out of range
Osheens-MacBook-Air-1115:co_assembler osheensachdev$ 


Traceback (most recent call last):
  File "Main.py", line 1, in <module>
    import pass_one
  File "/Users/osheensachdev/Documents/GitHub/co_assembler/pass_one.py", line 269, in <module>
    first_pass('code.txt')
  File "/Users/osheensachdev/Documents/GitHub/co_assembler/pass_one.py", line 123, in first_pass
    instruction = get_instruction(line)
  File "/Users/osheensachdev/Documents/GitHub/co_assembler/pass_one.py", line 183, in get_instruction
    assign_operands(instruction)
  File "/Users/osheensachdev/Documents/GitHub/co_assembler/pass_one.py", line 239, in assign_operands
    put_in_symbol_table(instruction['operands'][0], instruction["opcode"]["TYPE OF OPERAND"], None)
IndexError: list index out of range

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
        'TYPE OF OPERAND': 'VARIABLE',
    },
    'SAC': {
        'CODE': '0010', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'VARIABLE',
    },
    'ADD': {
        'CODE': '0011', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'VARIABLE'
    },
    'SUB': {
        'CODE': '0100', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'VARIABLE'
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
        'TYPE OF OPERAND': 'VARIABLE'
    },
    'DSP': {
        'CODE': '1001', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'VARIABLE'
    },
    'MUL': {
        'CODE': '1010', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'VARIABLE'
    },
    'DIV': {
        'CODE': '1011', 
        'NUMBER OF OPERANDS': 1,
        'TYPE OF OPERAND': 'VARIABLE'
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
    start_flag = False
    end_flag = False
    
    with open('code.txt') as file:
        for line in file: 
            line = line.strip()
            if line == '':
                continue

            if start_flag == False: 
                if line.split()[0] != "START":
                    continue
                if len(line.split()) != 2:
                    raise Exception("Exception : More than one or zero operands found!!")
                start_flag = True
                try:
                    location_counter = int(line.split()[1])
                except :
                    raise Exception("Exception : Wrong Address")
                continue
            if line == 'END':
              break

            instruction = get_instruction(line)
            instructions[instruction['location']] = instruction

    check_symbol_table()
    check_for_stop()
    assign_memory_to_variables()
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
        put_in_symbol_table(label, 'LABEL', instruction['location'])
    
    # Split line into opcode and operands
    words = list(line.split())
    instruction['mnemonic'] = words[0]
    instruction['operands'] = words[1:]

    # Look up mnemonic in opcode table and assign information about the opcode
    assign_opcode(instruction)
    assign_operands(instruction)

    return instruction

def put_in_symbol_table(symbol, symbol_type, address):
    """
        Check if the format of label is correct.
        Input: Label in string format
        Returns : Label in correct string format
        It raises and exception if label is not correct
        # Currently not implemented
    """
    global symbol_table
    
    if symbol in symbol_table:
        if symbol_table[symbol]['TYPE'] != symbol_type:
            raise Exception('Exception: ' + symbol + 'used as LABEL and VARIABLE both')

    if address == None:
        if symbol in symbol_table:
            return
        else:
            symbol_table[symbol] = {'TYPE': symbol_type, 'ADDRESS': address}
            return

    if symbol in symbol_table and symbol_table[symbol]['ADDRESS'] != None and address != None:
        raise Exception('Exception: ' + symbol + ' declared multiple times')
    else:
        symbol_table[symbol] = {'TYPE': symbol_type, 'ADDRESS':address}
    
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
    
    if instruction["opcode"]["NUMBER OF OPERANDS"] == 1:
        put_in_symbol_table(instruction['operands'][0], instruction["opcode"]["TYPE OF OPERAND"], None)


def check_symbol_table():
    global symbol_table
    
    for symbol in symbol_table:
        if symbol_table[symbol]['TYPE'] == 'LABEL' and symbol_table[symbol]["ADDRESS"] == None:
            raise Exception(symbol + " not defined")
    return True

def check_for_stop():
    global location_counter
    global instructions
    if instructions[location_counter - 1]['mnemonic'] != 'STP':
        raise Exception("STP Missing at end of code")

def createJSON(nameOfFile, dict_data):
    with open(nameOfFile+'.json', 'w') as json_file:
        json.dump(dict_data, json_file)

def assign_memory_to_variables():
    global location_counter
    global symbol_table
    for symbol in symbol_table:
        if symbol_table[symbol]['TYPE'] == 'VARIABLE':
            symbol_table[symbol]["ADDRESS"] = location_counter
            location_counter += 1

first_pass('code.txt')