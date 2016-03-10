from __future__ import print_function
from Word import *
target_file = None;
def disassembleInstruction(instruction):
	op = instruction['op']
	if op == 0b100000 :# R Type, many cases
		func = instruction['func']
		if   func == 0b000000: return SLL(instruction)	# SLL or NOP
		elif func == 0b000010: return SRL(instruction)	# SRL
		elif func == 0b001000: return JR(instruction)	# JR
		elif func == 0b100000: return ADD(instruction)	# ADD
		elif func == 0b100010: return SUB(instruction)	# SUB
		elif func == 0b100100: return AND(instruction)  # AND
		elif func == 0b100101: return OR(instruction)	# OR
		elif func == 0b001010: return MOVZ(instruction) # MOVZ
		elif func == 0b001101: return BREAK(instruction)#BREAK
		else :				   return INVALID(instruction)
	elif op == 0b111100: return MUL(instruction)	#MUL
	elif op == 0b100001: return BLTZ(instruction)	#BLTZ
	elif op == 0b100010: return J(instruction)		#J
	elif op == 0b100100: return BEQ(instruction)	#BEQ
	elif op == 0b101000: return ADDI(instruction)	#ADDI
	elif op == 0b100011: return LW(instruction) 	#LW
	elif op == 0b101011: return SW(instruction)  	#SW
	else:				 return INVALID(instruction)
		
def disassembleSet(set):
	n = 0
	for i in set:
		shouldBreak = disassembleInstruction(i)
		n += 1
		if(shouldBreak): break
	for i in range(n, len(set)):
		displayDataValue(set[i])
		
def SW(instruction):
	printInstructionAsBinary(instruction)
	print ("SW\tR",instruction['rt'], " ", instruction['immed'], "(R",instruction['rs'],")", sep="", file=target_file)
	return False
def LW(instruction):
	printInstructionAsBinary(instruction)
	print ("LW\tR",instruction['rt'], " ", instruction['immed'], "(R",instruction['rs'],")", sep="", file=target_file)
	return False
def ADDI(instruction):
	printInstructionAsBinary(instruction)
	print ("ADDI\tR",instruction['rt'], ", R",instruction['rs'],", #",instruction['immed'], sep="", file=target_file) #Use rt for rd since this is an i type
	return False
def BEQ(instruction):
	printInstructionAsBinary(instruction)
	print ("BEQ\tR",instruction['rt'], ", R",instruction['rs'],", #",instruction['immed'], sep="", file=target_file) #Use rt for rd since this is an i type
	return False
def J(instruction):
	printInstructionAsBinary(instruction)
	print ("J\t#", instruction['addr'] << 2, sep="", file=target_file)
	return False
def BLTZ(instruction):
	printInstructionAsBinary(instruction)
	print ("BLTZ\tR",instruction['rs'], ", #",instruction['immed'] << 2, sep="", file=target_file)
	return False
def MUL(instruction):
	printInstructionAsBinary(instruction)
	print ("MUL\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt'], sep="", file=target_file)
	return False
def BREAK(instruction):
	printInstructionAsBinary(instruction)
	print ('BREAK', file=target_file)
	return True
def MOVZ(instruction):
	printInstructionAsBinary(instruction)
	print ("MOVZ\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt'], sep="", file=target_file)
	return False
def INVALID(instruction):
	printInstructionAsBinary(instruction)
	print ('Invalid Instruction', file=target_file)
	return False
def SLL(instruction): #Could also be NOP, check included
	printInstructionAsBinary(instruction)
	if(instruction.word & (2**31 - 1) == 0):
		print("NOP", file=target_file)
	else:
		print ("SLL\tR",instruction['rd'], ", R",instruction['rt'],", #",instruction['sa'], sep="", file=target_file)
	return False
def SRL(instruction):
	printInstructionAsBinary(instruction)
	print ("SRL\tR",instruction['rd'], ", R",instruction['rt'],", #",instruction['sa'], sep="", file=target_file)
	return False
def ADD(instruction):
	printInstructionAsBinary(instruction)
	print ("ADD\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt'], sep="", file=target_file)
	return False
def SUB(instruction):
	printInstructionAsBinary(instruction)
	print ("SUB\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt'], sep="", file=target_file)
	return False
def AND(instruction):
	printInstructionAsBinary(instruction)
	print ("AND\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt'], sep="", file=target_file)
	return False
def OR(instruction) :
	printInstructionAsBinary(instruction)
	print ("OR\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt'], sep="", file=target_file)
	return False
def JR(instruction) :
	printInstructionAsBinary(instruction)
	print ("JR\tR", instruction['rs'], sep="", file=target_file)
	return False
def displayDataValue(word):
	for i in xrange(31, -1, -1): #decrement value
		print((word.word & 2**i) >> i, end="", file=target_file)
	print("\t",word.addr,"\t" , word.word, sep = "", file=target_file)
def printInstructionAsBinary(instruction):
	for i in xrange(31, -1, -1): #decrement value
		print((instruction.word & 2**i) >> i, end=" " if (i == 31 or i == 26 or i == 21 or i == 16 or i == 11 or i == 6) else "", file=target_file)
	print("\t", instruction.addr, "\t", end="", sep = "", file=target_file)