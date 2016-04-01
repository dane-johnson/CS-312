from word import *
import pdb

class Machine:
	DEFAULT_INIT_PC = 96 #We always start at 96 for some reason
	def __init__(self, fileName):
		self.fileName = fileName
		self.register = [0] * 32 #Creates an array of 32 values, initialized at 0 for all
		self.instructions = []
		self.PC = Machine.DEFAULT_INIT_PC
		self.lastPC = -1
		self.currLineDis = "INVALID"
		self.printOut = True
	
	def writeState(self, cycle):
		str = '=' * 20 + '\n'
		str += 'cycle:%d %d\t%s\n\n' % (cycle, self.lastPC, self.currLineDis)
		str += 'registers:\n'
		for i, v in enumerate(self.register):
			if(i % 8 == 0):
				str += 'r%02d:' % i
			str += '\t%d' % v
			if(i % 8 == 7):
				str += '\n'
		str += 'data:\n'
		dataAddr = self.findDataAddress()
		for i, instruction in enumerate(self.instructions[dataAddr:]):
			if(i % 8 == 0):
				str += '%02d:' % instruction.addr
			str += '\t%d' % instruction.word
			if(i % 8 == 7):
				str += '\n'
		str += '\n'
		self.file.write(str)
	
	def loadInstructions(self, instructions):
		self.instructions = instructions;
		
	def findDataAddress(self):
		for i, instruction in enumerate(self.instructions):
			if instruction['op'] == 0b100000 and instruction['func'] == 0b001101:
				return i + 1
		return len(instructions)
		
		
	def execute(self, instruction):
		#print bin(instruction.word) #for debugging
		op = instruction['op']
		if op == 0b100000 :# R Type, many cases
			func = instruction['func']
			if   func == 0b000000: return self.SLL(instruction)		# SLL or NOP
			elif func == 0b000010: return self.SRL(instruction)		# SRL
			elif func == 0b001000: return self.JR(instruction)		# JR
			elif func == 0b100000: return self.ADD(instruction)		# ADD
			elif func == 0b100010: return self.SUB(instruction)		# SUB
			elif func == 0b100100: return self.AND(instruction)  # AND
			elif func == 0b100101: return self.OR(instruction)		# OR
			elif func == 0b001010: return self.MOVZ(instruction) # MOVZ
			elif func == 0b001101: return self.BREAK(instruction)#BREAK
			else :				   return self.INVALID(instruction)
		elif op == 0b111100: return self.MUL(instruction)		#MUL
		elif op == 0b100001: return self.BLTZ(instruction)		#BLTZ
		elif op == 0b100010: return self.J(instruction)				#J
		elif op == 0b100100: return self.BEQ(instruction)		#BEQ
		elif op == 0b101000: return self.ADDI(instruction)		#ADDI
		elif op == 0b100011: return self.LW(instruction) 		#LW
		elif op == 0b101011: return self.SW(instruction)  		#SW
		else:				 return self.INVALID(instruction)
		
	def executeInstructions(self):
		self.file = open(self.fileName, 'w')
		shouldBreak = False
		cycle = 0
		while not shouldBreak:
			i = self.findInstruction(self.PC)
			self.lastPC = self.PC
			shouldBreak = self.execute(self.instructions[i])
			if(self.printOut):
				cycle += 1
				self.writeState(cycle)
			self.PC += 4
			self.printOut = True
		self.PC = Machine.DEFAULT_INIT_PC
		self.file.close()
		
	def findInstruction(self, addr):
		#pdb.set_trace()
		min, max = 0, len(self.instructions) - 1
		pivot = len(self.instructions) / 2
		while(pivot >= min and pivot <= max):
			if(self.instructions[pivot].addr == addr): return pivot
			elif(self.instructions[pivot].addr > addr): max = pivot - 1
			else: min = pivot + 1
			pivot = min + len(self.instructions[min:max + 1]) / 2
		return -1;

	def SW(self, instruction):
		self.currLineDis = "SW\tR" + str(instruction['rt']) + ", " + str(instruction['immed']) + "(R" + str(instruction['rs'])+")"
		self.instructions[self.findInstruction(instruction['immed'] + self.register[instruction['rs']])].word = self.register[instruction['rt']]
		return False
	def LW(self, instruction):
		self.currLineDis = "LW\tR"+str(instruction['rt'])+ ", "+ str(instruction['immed'])+ "(R"+str(instruction['rs'])+")"
		self.register[instruction['rt']] = self.instructions[self.findInstruction(instruction['immed'] + self.register[instruction['rs']])].word
		return False
	def ADDI(self, instruction):
		self.currLineDis = "ADDI\tR"+str(instruction['rt'])+ ", R"+str(instruction['rs'])+", #"+str(instruction['immed']) #Use rt for rd since this is an i type
		self.register[instruction['rt']] += instruction['immed']
		return False
	def BEQ(self, instruction):
		self.currLineDis = "BEQ\tR"+str(instruction['rt'])+ ", R"+str(instruction['rs'])+", #",str(instruction['immed']) #Use rt for rd since this is an i type
		if self.register[instruction['rt']] == self.register[instruction['rs']]:
			this.PC = str(instruction['immed']) - 4
		return False
	def J(self, instruction):
		self.currLineDis = "J\t#"+ str(instruction['addr'] << 2)
		self.PC = (instruction['addr'] << 2) - 4
		return False
	def BLTZ(self, instruction):
		self.currLineDis = "BLTZ\tR"+str(instruction['rs'])+ ", #"+str(instruction['immed'] << 2)
		if self.register[instruction['rs']] < 0:
			self.PC += (instruction['immed'] << 2)
		return False
	def MUL(self, instruction):
		self.currLineDis = "MUL\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
		self.register[instruction['rd']] = self.register[instruction['rs']] * self.register[instruction['rt']]
		return False
	def BREAK(self, instruction):
		self.currLineDis = 'BREAK'
		return True
	def MOVZ(self, instruction):
		self.currLineDis = "MOVZ\tR"+str(instruction['rd'])+ ", R",str(instruction['rs'])+", R",str(instruction['rt'])
		if self.register[instruction['rt']] == 0:
			self.register[instruction['rd']] = self.register[instruction['rs']]
		return False
	def INVALID(self, instruction):
		self.currLineDis = 'Invalid Instruction'
		self.printOut = False
		return False
	def SLL(self, instruction): #Could also be NOP, check included
		if(instruction.word & (2**31 - 1) == 0):
			self.currLineDis = "NOP"
		else:
			self.currLineDis = "SLL\tR"+str(instruction['rd'])+ ", R"+str(instruction['rt'])+", #"+str(instruction['sa'])
			self.register[instruction['rd']] = self.register[instruction['rt']] << instruction['sa']
		return False
	def SRL(self, instruction):
		self.currLineDis = "SRL\tR"+str(instruction['rd'])+ ", R"+str(instruction['rt'])+", #"+str(instruction['sa'])
		self.register[instruction['rd']] = self.register[instruction['rt']] >> instruction['sa']
		return False
	def ADD(self, instruction):
		self.currLineDis = "ADD\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
		self.register[instruction['rd']] = self.register[instruction['rs']] + self.register[instruction['rt']]
		return False
	def SUB(self, instruction):
		self.currLineDis = "SUB\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
		self.register[instruction['rd']] = self.register[instruction['rs']] - self.register[instruction['rt']]
		return False
	def AND(self, instruction):
		self.currLineDis = "AND\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
		self.register[instruction['rd']] = self.register[instruction['rs']] & self.register[instruction['rt']]
		return False
	def OR(self, instruction) :
		self.currLineDis = "OR\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
		self.register[instruction['rd']] = self.register[instruction['rs']] | self.register[instruction['rt']]
		return False
	def JR(self, instruction) :
		self.currLineDis = "JR\tR"+ str(instruction['rs'])
		self.PC = self.register[instruction['rs']]
		return False
