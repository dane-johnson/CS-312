fileName = 'test1.bin'
import filemanager
(word, address) = filemanager.loadInstructionsAndAddresses(fileName)
instruction = []
from Word import Instruction
for i in range(len(word)):
	instruction.append(Instruction(word[i], address[i]))
import disassembler
disassembler.disassembleSet(instruction)