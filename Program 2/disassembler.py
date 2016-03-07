from Word import *
def disassemble(word):
	if(word.getOp() == 0): #RType instruction
		word = RType(instruction);
		print "RType Instruction Received"
	elif ((word.getOp() & 0b111110) == 0b000010): # JType
		word = JType(instruction);
		print "JType Instruction Received"
	else: #IType
		word = IType(instruction);
		print "IType Instruction Received"