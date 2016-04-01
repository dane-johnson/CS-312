import filemanager
import sys
import disassembler
from word import Instruction
from machine import Machine


def main(argv):
	
	if len(argv) < 5:
		print "Usage: mipssim.py -i [input_file_name] -o [output_file_name]"
		quit(-1)
	try:
		inputFilenameIndex = argv.index('-i') + 1
		outputFilenameIndex = argv.index('-o') + 1
	except ValueError:
		print "Usage: mipssim.py -i [input_file_name] -o [output_file_name]"
		quit(-1)
	
	infileName = argv[inputFilenameIndex]
	if '.bin' not in infileName:
		infileName+='.bin'
	outFileName = argv[outputFilenameIndex]
	
	(word, address) = filemanager.loadInstructionsAndAddresses(infileName)
	instruction = []
	for i in range(len(word)):
		instruction.append(Instruction(word[i], address[i]))
	
	disassembler.target_file = open(outFileName+'_dis.txt', 'w')
	disassembler.disassembleSet(instruction)
	mips = Machine(outFileName+'_sim.txt')
	mips.loadInstructions(instruction)
	mips.executeInstructions()
	
if __name__ == '__main__':
	main(sys.argv)