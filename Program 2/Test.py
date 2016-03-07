fileName = 'test2.bin'
import filemanager
(word, address) = filemanager.loadInstructionsAndAddresses(fileName)
instruction = []
from Word import Instruction
for i in range(len(word)):
	instruction.append(Instruction(word[i], address[i]))
from Machine import Machine
mips = Machine(address[0])
mips.loadInstructions(instruction)
mips.executeInstructions()