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
	
	locations = sorted(list(memory.keys()))
	with open('machine_code.txt', 'w') as file:
		for location in locations:
			location = '0' * (8 - len(bin(location)[2:])) + bin(location)[2:]
			file.write((location + ": " + memory[location] + "\n"))

def translate_instruction(instruction, symbol_table):
	translated_instruction = ''
	opcode = instruction['opcode']
	translated_instruction += opcode['CODE']
	if opcode['NUMBER OF OPERANDS'] == 0:
		translated_instruction += '00000000'
	else:
		if opcode['TYPE OF OPERAND'] == 'ADDRESS':
			translated_instruction += '0' * (8 - len(bin(int(instruction['operands'][0]))[2:])) + bin(int(instruction['operands'][0]))[2:]
			#+ bin(instruction['operands'][0])[2:]
		else:
			translated_instruction += (symbol_table[instruction['operands'][0]])
	return translated_instruction


second_pass()