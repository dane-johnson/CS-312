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
		if  ((instruction.getOp() & 0b100000) >> 5 == 0): 		#Invalid Instruction
			print "Invalid Instruction Received"
		elif((instruction.getOp() & 0b011111) == 0): 			#RType instruction
			print "RType Instruction Received"
		elif ((instruction.getOp() & 0b011110) == 0b000010): 	#JType
			print "JType Instruction Received"
		else: 													#IType
			print "IType Instruction Received"
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
