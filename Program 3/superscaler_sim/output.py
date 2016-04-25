from superscaler_sim.word import Instruction
def output(machine, file): #file should be an open, write textually file
  out = ''
  def p(x='', y = out): y += x + '\n' #quick helper function
  def bin(w):
    s = ''
    for i in range(31, -1, -1):
      s += str(w & (1 << i))
    return s
  p('-' * 20)
  p('Cycle %d:' % machine.cycleCount) #print the cycle
  p() #print a blank line
  if len(machine.preIssue) :
    p('Pre-Issue Buffer:')
    for i, k in enumerate(machine.preIssue.queue):
      p(('\tEntry %d:\t' % i)+dissassemble(k['instruction']))
  if len(machine.preAlu):
    p('Pre_ALU Queue:')
    for i, k in enumerate(machine.preALU.queue):
      p(('\tEntry %d:\t' % i)+dissassemble(k['instruction']))
  if len(machine.postAlu):
    p('Post_ALU Queue:')
    p(('\tEntry %d:\t' % 0)+dissassemble(machine.postAlu.entry['instruction']))
  if len(machine.preMem):
    p('Pre_MEM Queue:')
    for i, k in enumerate(machine.preMEM.queue):
      p(('\tEntry %d:\t' % i)+dissassemble(k['instruction']))
  if len(machine.postMem):
    p('Post_MEM Queue:')
    p(('\tEntry %d:\t' % 0)+dissassemble(machine.postMem.entry['instruction']))
  p() #print a blank line
  p('Registers:')
  for i, v in enumerate(machine.registers):
    if(i % 8 == 0):
      out += 'r%02d:' % i
    out += '\t%d' % v
    if(i % 8 == 7):
      p()
  for i, k in enumerate(machine.cache.sets):
    p('\tSet %d: LRU=%d' % (i, k.lru))
    for j, l in enumerate(k.entries):
      p('\tEntry %d: [(%d, %d, %d,)<%s,%s>]' % (j, l.v, l.d, l.tag, bin(l.words[0]), bin(l.words[1])))
  p()
  dataAddr = findDataAddress(machine)
  for i, instruction in enumerate(machine.memory.instructions[dataAddr:]):
    if(i % 8 == 0):
      out += '%02d:' % (96 + (dataAddr + i) * 4)
    out += '\t%d' % instruction
    if(i % 8 == 7):
      p()
  file.write(out)
def dissassemble(word):
  pass
def findDataAddress(machine):
    for i, instruction in enumerate(machine.memory.instructions):
      instruction = Instruction(instruction)
      if instruction['op'] == 0b100000 and instruction['func'] == 0b001101: #BREAK statement
        return i + 1
    return -1