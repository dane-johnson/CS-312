from word import *

class Machine:
	DEFAULT_INIT_PC = 96 #We always start at 96 for some reason
	def __init__(self, initialAddress = 0):
		self.initialAddress = initialAddress
		self.register = [0] * 32 #Creates an array of 32 values, initialized at 0 for all
		self.instructions = []
		self.PC = DEFAULT_INIT_PC
		self.currLineDis = "INVALID"
		
	def loadInstructions(self, instructions):
		self.instructions = instructions;
		
	def execute(self, instruction):
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
		while(self.register[PC] < self.instructions[-1].addr):
			i = self.findInstruction(self.register[PC])
			self.execute(self.instructions[i])
			self.execute(self.instructions[i])
			self.register[PC] += 4;
		self.register[PC] = self.initialAddress;
	def findInstruction(self, addr):
		min, max = 0, len(self.instructions) - 1
		pivot = len(self.instructions) / 2
		while(pivot >= min and pivot <= max):
			if(self.instructions[pivot].addr == addr): return pivot
			elif(self.instructions[pivot].addr > addr): max = pivot - 1
			else: min = pivot + 1
		return -1;

	def SW(self, instruction):
		self.currLineDis = "SW\tR",instruction['rt'], ", ", instruction['immed'], "(R",instruction['rs'],")"
		return False
	def LW(self, instruction):
		self.currLineDis = "LW\tR",instruction['rt'], ", ", instruction['immed'], "(R",instruction['rs'],")"
		return False
	def ADDI(self, instruction):
		self.currLineDis = "ADDI\tR",instruction['rt'], ", R",instruction['rs'],", #",instruction['immed'] #Use rt for rd since this is an i type
		return False
	def BEQ(self, instruction):
		self.currLineDis = "BEQ\tR",instruction['rt'], ", R",instruction['rs'],", #",instruction['immed'] #Use rt for rd since this is an i type
		return False
	def J(self, instruction):
		self.currLineDis = "J\t#", instruction['addr'] << 2
		return False
	def BLTZ(self, instruction):
		self.currLineDis = "BLTZ\tR",instruction['rs'], ", #",instruction['immed'] << 2
		return False
	def MUL(self, instruction):
		self.currLineDis = "MUL\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt']
		return False
	def BREAK(self, instruction):
		self.currLineDis = 'BREAK', file=target_file)
		return True
	def MOVZ(self, instruction):
		self.currLineDis = "MOVZ\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt']
		return False
	def INVALID(self, instruction):
		self.currLineDis = 'Invalid Instruction'
		return False
	def SLL(self, instruction): #Could also be NOP, check included
		if(instruction.word & (2**31 - 1) == 0):
			self.currLineDis = "NOP"
		else:
			self.currLineDis = "SLL\tR",instruction['rd'], ", R",instruction['rt'],", #",instruction['sa']
		return False
	def SRL(self, instruction):
		self.currLineDis = "SRL\tR",instruction['rd'], ", R",instruction['rt'],", #",instruction['sa']
		return False
	def ADD(self, instruction):
		self.currLineDis = "ADD\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt']
		return False
	def SUB(self, instruction):
		self.currLineDis = "SUB\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt']
		return False
	def AND(self, instruction):
		self.currLineDis = "AND\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt']
		return False
	def OR(self, instruction) :
		self.currLineDis = "OR\tR",instruction['rd'], ", R",instruction['rs'],", R",instruction['rt']
		return False
	def JR(self, instruction) :
		self.currLineDis = "JR\tR", instruction['rs']
		return False
