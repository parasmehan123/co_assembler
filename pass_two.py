
def get_binary_address(address):
	"""
    Returns the 8 bit binary address in string form from an integer address in decimal form
    Input: address - int
    Returns: binary address - string
    """
	return '0' * (8 - len(bin(address)[2:])) + bin(address)[2:]
  

import json

memory = {}

def second_pass():
	"""
    Executes second pass of assembly process
    Input : None
    Returns : None
    """
	temp_file = json.load(open('temp_file.json'))
	symbol_table = temp_file['symbol_table']
	instructions = temp_file['instructions']

    # assign physical memory space to each instruction
	for location in instructions:
		instruction = instructions[location]
		translated_instruction = translate_instruction(instruction, symbol_table)
		memory[instruction['location']] = translated_instruction

	# assign physical memory space to each variable
	for symbol in symbol_table:
		if symbol_table[symbol]['TYPE'] == 'VARIABLE':
			memory[symbol_table[symbol]['ADDRESS']] = 'XXXXXXXXXXXX'

    # write the location: memory[location] for each location in memory into a final ouput file
	locations = sorted(list(memory.keys()))
	with open('machine_code.txt', 'w') as file:
		for location in locations:
			file.write((get_binary_address(location) + ": " + memory[location] + "\n"))

def translate_instruction(instruction, symbol_table):
	"""
	Function to Translate instructions in binary form.
	Input : instruction,symbol_table
	return : translated_instruction : String
	
	"""
	translated_instruction = ''
	opcode = instruction['opcode']
	translated_instruction += opcode['CODE']
	if opcode['NUMBER OF OPERANDS'] == 0:
		translated_instruction += '00000000'
	else:
		translated_instruction += get_binary_address(symbol_table[instruction['operands'][0]]['ADDRESS'])
	return translated_instruction


second_pass()