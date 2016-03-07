from Word import *

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
		if(word.getOp() == 0): #RType instruction
			word = RType(instruction);
			print "RType Instruction Received"
		elif ((word.getOp() & 0b111110) == 0b000010): # JType
			word = JType(instruction);
			print "JType Instruction Received"
		else: #IType
			word = IType(instruction);
			print "IType Instruction Received"
	def executeInstructions(self):
		while(self.register[PC] < self.instructions[-1]):
			self.execute(self.instructions[self.register[PC]]);#Read in the next 4 bytes as 1 word
			self.register[PC] += 1;
		self.register[PC] = self.initialAddress;

PC = 1;