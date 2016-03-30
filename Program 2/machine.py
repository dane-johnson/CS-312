from word import *

class Machine:
	initialAddress = 0
	register = [0] * 32 #Creates an array of 32 values, initialized at 0 for all
	instructions = []
	
	def __init__(self, initialAddress):
		self.initialAddress = initialAddress
		self.register[PC] = initialAddress;
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

PC = 1;
