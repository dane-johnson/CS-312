import os
import struct
# convert ints to signed 
def imm32BitUnsignedTo32BitSignedConverter( num ):
	negBitMask = 0x80000000
	if( negBitMask & num ) > 0 :
		num = num ^ 0xFFFFFFFF
		num = num + 1
		num = num * -1
	return num

inputFileName = 'test2.bin'	

# how to read binary file and get ints
inFile = open( inputFileName, 'rb' )	

# get the file length
inFileLen = os.stat( inputFileName )[6]
inFileWords = inFileLen / 4

instructions = []
address = []
# read the words from the file
for i in range( inFileWords ) :
	instructions.append( struct.unpack('>I', inFile.read(4))[0] )
	address.append( 96 + (i*4) )

inFile.close()