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

memory = {i: '000000000000' for i in range(100000)}

def pass_two():
	temp_file = json.load('temp_file.json')
	symbol_table = temp_file['symbol_table']
	instructions = temp_file['instructions']

	for location in instructions:
		instruction = instructions[location]
		translated_instruction = translate_instruction(instruction)
		memory[instructions['location']] = translated_instruction

def translate_instruction(instruction):
	translated_instruction = ''
	opcode = instruction['opcode']
	translated_instruction += opcode['CODE']
	if opcode['NUMBER OF OPERANDS'] == 0:
		translated_instruction += '00000000'
	else:
		if opcode['TYPE OF OPERAND'] == 'ADDRESS':
			translated_instruction += instructions['operands'][0]
		else:
			translated_instruction += symbol_table[instructions['operands'][0]]
	return translated_instruction