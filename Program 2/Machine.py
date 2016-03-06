from Word import *

class Machine:
	register = [0] * 32; #Creates an array of 32 values, initialized at 0 for all
	instructions = [];
	
	def loadInstructions(self, instructions):
		self.instructions = instructions;
	def execute(self, instruction):
		word = Word(instruction);
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
		while(self.register[PC] < len(self.instructions)):
			self.execute(self.instructions[self.register[PC]:self.register[PC] + 4]);#Read in the next 4 bytes as 1 word
			self.register[PC] += 4;
		self.register[PC] = 0;

PC = 1;