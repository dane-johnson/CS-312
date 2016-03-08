from Word import *
def disassembleInstruction(instruction):
	op = instruction['op']
	if op == 0b100000 :# R Type, many cases
		func = instruction['func']
		if   func == 0b000000: return SLL()	# SLL
		elif func == 0b000010: return SRL()	# SRL
		elif func == 0b001000: return JR()	# JR
		elif func == 0b100000: return ADD()	# ADD
		elif func == 0b100010: return SUB()	# SUB
		elif func == 0b100100: return AND() # AND
		elif func == 0b100101: return OR()	# OR
		elif func == 0b001010: return MOVZ()# MOVZ
		elif func == 0b001101: return BREAK()#BREAK
		else :				   return NOP()
	elif op == 0b111100: return MUL()	#MUL
	elif op == 0b100001: return BLTZ()	#BLTZ
	elif op == 0b100010: return J()		#J
	elif op == 0b100100: return BEQ()	#BEQ
	elif op == 0b101000: return ADDI()	#ADDI
	elif op == 0b100011: return LW() 	#LW
	elif op == 0b101011: return SW()  	#SW
	else:				 return NOP()
		
def disassembleSet(set):
	n = 0
	for i in set:
		shouldBreak = disassembleInstruction(i)
		n += 1
		if(shouldBreak): break
	for i in range(n, len(set)):
		displayDataValue(set[i])
		
def SW():
	print 'SW'
	return False
def LW():
	print 'LW'
	return False
def ADDI():
	print 'ADDI'
	return False
def BEQ():
	print 'BEQ'
	return False
def J():
	print 'J'
	return False
def BLTZ():
	print 'BLTZ'
	return False
def MUL():
	print 'MUL'
	return False
def BREAK():
	print 'BREAK'
	return True
def MOVZ():
	print 'MOVZ'
	return False
def NOP():
	return False
def SLL():
	print 'SLL'
	return False
def SRL():
	print 'SRL'
	return False
def ADD():
	print 'ADD'
	return False
def SUB():
	print 'SUB'
	return False
def AND():
	print 'AND'
	return False
def OR() :
	print 'OR'
	return False
def JR() :
	print 'JR'
	return False
def displayDataValue(word):
	print word.word