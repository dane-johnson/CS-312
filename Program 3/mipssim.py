from superscaler_sim.machine import Machine
from superscaler_sim.output import output as out
import disassembler

import os
import struct
import sys

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
  infile = open(infileName, 'rb')
  infileLen = os.stat(infileName)[6]
  infileWords = infileLen / 4
  
  instructions = []
  for i in range(infileWords):
    instructions.append(struct.unpack('>I', infile.read(4))[0])
  mips = Machine(instructions)
  
  with open(outFileName+'_dis.txt', 'wt') as f:
    disassembler.target_file = f
    disassembler.disassembleSet(instructions)
  
  
  outputfilename = outFileName+'_pipeline.txt'
  outputfile = open(outputfilename, 'wt')
  mips.executeMix(out, mips, outputfile)
  outputfile.close()

if __name__ == '__main__':
  main(sys.argv)