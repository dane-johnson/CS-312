import os
import struct
def loadInstructionsAndAddresses(inputFileName):
	inFile = open( inputFileName, 'rb' )	
	
	# get the file length
	inFileLen = os.stat( inputFileName )[6]
	inFileWords = inFileLen / 4
	
	instructions = []
	address = []
	# read the words from the file
	for i in range( inFileWords ) :
		instructions.append(struct.unpack('>I', inFile.read(4))[0] )
		address.append( 96 + (i*4) )

	inFile.close()
	return (instructions, address)
