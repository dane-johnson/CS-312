from Word import *
def disassembleWord(instruction):
	if  ((instruction.getOp() & 0b100000) >> 5 == 0): 		#Invalid Instruction
		print "Invalid Instruction Received"
	elif((instruction.getOp() & 0b011111) == 0): 			#RType instruction
		print "RType Instruction Received"
	elif ((instruction.getOp() & 0b011110) == 0b000010): 	#JType
		print "JType Instruction Received"
	else: 													#IType
		print "IType Instruction Received"
		
def disassembleSet(set):
	for i in set:
		disassembleWord(i)
def disassembleRType(instruction):
	{
		0b1000000: pass # ADD instruction
		0b1000010: pass # SUB instruction
		0b0000000: pass # SLL instruction
		0b0000010: pass # SRL instruction
		
	}[instruction['func']]