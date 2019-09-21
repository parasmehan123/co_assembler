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

def evaluate_comment():

evaluate = {'comment': evaluate_comment, 'unary': evaluate_unary, 'binary': evaluate_binary}

OPCODE = {
	'CLA':'0000', 
	'LAC': '0001', 
	'SAC': '0010', 
	'ADD': '0011', 
	'SUB': '0100', 
	'BRZ': '0101', 
	'BRN': '0110',
	'BRP': '0111',
	'INP': '1000',
	'DSP': '1001',
	'MUL': '1010',
	'DIV': '1011',
	'STP': '1100',
}

def pass_two(input, symbol_table):
	code = {}
	location_counter = 0
	for instruction in input:
		if instruction['type'] == 'comment:
			continue
		if instruction['type']
			code = OPCODE[instruction['opcode']]
			