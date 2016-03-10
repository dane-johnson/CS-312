import filemanager
import sys
if len(sys.argv) < 3:
	print "Usage: Main.py [input_file_name] [output_file_name]"
	quit(-1)
inFileName = sys.argv[1]
outFileName = sys.argv[2]
(word, address) = filemanager.loadInstructionsAndAddresses(inFileName)
instruction = []
from Word import Instruction
for i in range(len(word)):
	instruction.append(Instruction(word[i], address[i]))
import disassembler
disassembler.target_file = open(outFileName, 'wt')
disassembler.disassembleSet(instruction)