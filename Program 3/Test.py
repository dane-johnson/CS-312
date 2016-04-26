from superscaler_sim.machine import Machine
from superscaler_sim.output import output as out
import disassembler

import os
import struct

def main():
  inputfilename = 't2.bin'
  infile = open(inputfilename, 'rb')
  infileLen = os.stat(inputfilename)[6]
  infileWords = infileLen / 4
  
  instructions = []
  for i in range(infileWords):
    instructions.append(struct.unpack('>I', infile.read(4))[0])
  mips = Machine(instructions)
  
  with open('t2_dis.txt', 'wt') as f:
    disassembler.target_file = f
    disassembler.disassembleSet(instructions)
  
  
  outputfilename = 't2_pipeline.txt'
  outputfile = open(outputfilename, 'wt')
  mips.executeMix(out, mips, outputfile)
  outputfile.close()

if __name__ == '__main__':
  main()