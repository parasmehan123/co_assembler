'''
TODO:
    Add the word 'Exception'
'''


'''

01100100: 000000000000
01100101: 100001110001
01100110: 100001110010
01100111: 000101110001
01101000: 010001110010
01101001: 011001101101
01101010: 100101110001
01101011: 000000000000
01101100: 010101110000
01101101: 100101110010
01101110: 000000000000
01101111: 010101110000
01110000: 110000000000
01110001: XXXXXXXX
01110010: XXXXXXXX



'''
'''
Input: input - list of dictionaries, each dictionary corresponds to one line of code and has fields:
[
	'is_comment',
	'opcode', 
	'length', 
	'line'
]

Function:
converts the input to object code

Return: None
'''

def get_binary_address(address):
	return '0' * (8 - len(bin(address)[2:])) + bin(address)[2:]
  

import json

memory = {}

def second_pass():
	temp_file = json.load(open('temp_file.json'))
	symbol_table = temp_file['symbol_table']
	instructions = temp_file['instructions']

	for location in instructions:
		instruction = instructions[location]
		translated_instruction = translate_instruction(instruction, symbol_table)
		memory[instruction['location']] = translated_instruction

	for symbol in symbol_table:
		if symbol_table[symbol]['TYPE'] == 'VARIABLE':
			memory[symbol_table[symbol]['ADDRESS']] = 'XXXXXXXXXXXX'

            
	locations = sorted(list(memory.keys()))
	with open('machine_code.txt', 'w') as file:
		for location in locations:
			file.write((get_binary_address(location) + ": " + memory[location] + "\n"))

def translate_instruction(instruction, symbol_table):
	translated_instruction = ''
	opcode = instruction['opcode']
	translated_instruction += opcode['CODE']
	if opcode['NUMBER OF OPERANDS'] == 0:
		translated_instruction += '00000000'
	else:
		translated_instruction += get_binary_address(symbol_table[instruction['operands'][0]]['ADDRESS'])
	return translated_instruction


second_pass()