from Word import *

class Machine:
	register = [0] * 32; #Creates an array of 32 values, initialized at 0 for all
	instructions = [];
	currentLine = 0;
	
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
		while(self.currentLine < len(self.instructions)):
			self.execute(self.instructions[self.currentLine]);
			self.currentLine += 1;
			