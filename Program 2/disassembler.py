from Word import *
def disassembleInstruction(instruction):
	shouldBreak = {
		0b100000: # R Type, many cases
		{
			0b000000: False, # SLL
			0b000010: False, # SRL
			0b001000: False, # JR
			0b100000: False, # ADD
			0b100010: False, # SUB
			0b100100: False, # AND
			0b100101: False, # OR
			0b001010: False, # MOVZ
			0b001101: True  #BREAK
		}.get(instruction['func'], NOP()),
		0b111100: False, #MUL
		0b100001: False, #BLTZ
		0b100010: False, # J
		0b100100: False, #BEQ
		0b101000: False, #ADDI
		0b100011: False, #LW
		0b101011: False  #SW
	}.get(instruction['op'], NOP())
	return shouldBreak
		
def disassembleSet(set):
	n = 0
	for i in set:
		shouldBreak = disassembleInstruction(i)
		n += 1
		if(shouldBreak): break
	for i in range(n, len(set)):
		displayDataValue(set[i])
		
def NOP():
	return False;
def displayDataValue(word):
	print bin(word.word)