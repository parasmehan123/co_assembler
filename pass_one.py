

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
line_number = 0
success = True

def first_pass():
    """
        Executes pass one of the assembler.
        Input: FIle name for which code needs to be translated 
        Return: None
    """

    global temp_file
    global instructions
    global symbol_table
    global line_number
    global location_counter
    global success

    instructions = {}
    symbol_table = {}
    location_counter = 0
    start_flag = False
    end_flag = False
    
    with open("code.txt") as file:
        for line in file: 
            line_number += 1
            line = line.strip()
            if line == '':
                continue

            # Wait for "START" Assembler directive
            if start_flag == False: 
                if line.split()[0] != "START":
                    continue
                if len(line.split()) != 2:
                    raise Exception("Exception : START Assembler directive supplied with wrong number of operands")
                start_flag = True
                try:
                    location_counter = int(line.split()[1])
                except :
                    raise Exception("Exception : Wrong Address")
                continue
            # If END Assembler directive found stop reading
            if line == 'END':
                end_flag = True
                break

            # Process each instruction of the Assembly language code
            instruction = get_instruction(line)
            instructions[instruction['location']] = instruction
    if start_flag == False:
        raise Exception("Exception: START not found!")
    if end_flag == False:
        raise Exception("Exception: END not found")
    # Once all instructions have been processed check if symbol table has any label without an address
    check_symbol_table()
    # Check if code contains stop or not
    check_for_stop()
    # Assign memory to all the variables used in Assembly Language
    assign_memory_to_variables()
    # Save all pass one output into a file.
    temp_file = {'instructions': instructions, 'symbol_table': symbol_table, 'success': success}
    print('tempfile:' , temp_file)
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
        Exceptions:
        #1  When Label format is not correct
        #2  When the OP/CODE is not correct

    """

    global line_number
    global location_counter

    instruction = {
        "line_number": None,
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


    # Assign line number to instruction
    instruction['line_number'] = line_number

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
        Insert symbol, symbol type and its address into the symbol table
        Input: symbol - string , symbol type- string, address- int
        Returns : None
        Exceptions:
            #1  Symbol declared multiple times
            #2  Same name used as a variable and label both
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
        Exception:
            #1  invalid opcode - no matching opcode found in opcode table
    """
    opcode = instruction['mnemonic']

    if opcode in opcodes:
        instruction['opcode'] = opcodes[opcode]
    else:
        raise Exception( 'Exception: (Line No. ' + str(instruction['line_number']) + ') ' + opcode + ' not a valid opcode')
    
def assign_operands(instruction):
    """
        Checks for operands and insert in symbol table
        Input : instruction
        Returns : None
        Exceptions:
            #1  if Opcode supplied with wrong number of operands.
    """

    if len(instruction["operands"]) != instruction["opcode"]["NUMBER OF OPERANDS"]:
        raise Exception('Exception: (Line No. ' + str(instruction['line_number']) + ') ' + "Opcode supplied with wrong number of operands")
    
    if instruction["opcode"]["NUMBER OF OPERANDS"] == 1:
        put_in_symbol_table(instruction['operands'][0], instruction["opcode"]["TYPE OF OPERAND"], None)

def check_symbol_table():
    """
    Check if any label in symbol table has not been defined in the code
    Input : None
    Returns : None
    Exceptions : 
        #1 if Label is not defined.
    
    """
    global symbol_table
    
    for symbol in symbol_table:
        if symbol_table[symbol]['TYPE'] == 'LABEL' and symbol_table[symbol]["ADDRESS"] == None:
            raise Exception(symbol + " not defined")
    return True

def check_for_stop():
    """
    Check if STP is missing at the end of code or not.
    Input : None
    Returns : None
    Exceptions : 
        #1  STP Missing at end of code.
    """
    global location_counter
    global instructions

    if (location_counter - 1) not in instructions or instructions[location_counter - 1]['mnemonic'] != 'STP':
        raise Exception("STP Missing at end of code")

def assign_memory_to_variables():
    """
    Assign memory 
    Input : None
    Returns : None
    Exceptions : 
      
    """
    global location_counter
    global symbol_table
    for symbol in symbol_table:
        if symbol_table[symbol]['TYPE'] == 'VARIABLE':
            symbol_table[symbol]["ADDRESS"] = location_counter
            location_counter += 1
            
def createJSON(nameOfFile, dict_data):
    """
    Save dictionary as a json file
    Input: nameOfFile - string, dict_data - dictionary
    Returns: None
    """
    with open(nameOfFile+'.json', 'w') as json_file:
          json.dump(dict_data, json_file)


