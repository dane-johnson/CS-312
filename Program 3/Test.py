from superscaler_sim.machine import Machine
import superscaler_sim.output as out

import os
import struct

def main():
  inputfilename = 'test1.bin'
  infile = open(inputfilename, 'rb')
  infileLen = os.stat(inputfilename)[6]
  infileWords = infileLen / 4
  
  instructions = []
  for i in range(infileWords):
    instructions.append(struct.unpack('>I', infile.read(4))[0])
  
  mips = Machine(instructions)
  
  outputfilename = 'test1_sim.txt'
  outputfile = open(outputfilename, 'wt')
  mips.executeMix()
  outputfile.close()

if __name__ == '__main__':
  main()