from superscaler_sim.word import Instruction
from superscaler_sim.word import Word
def output(machine, file): #file should be an open, write textually file
  out = ['']
  def p(x=''): out[0] += x + '\n' #quick helper function
  def bin(w):
    s = ''
    for i in range(31, -1, -1):
      s += str((w >> i) & 1)
    return s
  p('-' * 20)
  #p(str(machine.pc))
  p('Cycle:%d' % machine.cycleCount) #print the cycle
  p() #print a blank line
  p('Pre-Issue Buffer:')
  #for i, k in enumerate(machine.preIssue.buffer):
  for i in range(4):
    if i < len(machine.preIssue):
      k = machine.preIssue.buffer[i]
      p(('\tEntry %d:\t' % i)+'['+dissassemble(k)+']')
    else :
      p(('\tEntry %d:\t') %i)
  p('Pre_ALU Queue:')
  for i in range(2):
    if i < len(machine.preAlu):
      k = machine.preAlu.queue[(i + 1) * -1]['instruction']
      p(('\tEntry %d:\t' % i)+'['+dissassemble(k)+']')
    else :
      p(('\tEntry %d:\t') %i)
  p('Post_ALU Queue:')
  if len(machine.postAlu):
    p(('\tEntry %d:\t' % 0)+'['+dissassemble(machine.postAlu.entry['instruction'])+']')
  else:
    p('\tEntry %d:\t' % 0)
  p('Pre_MEM Queue:')
  for i in range(2):
    if i < len(machine.preMem):
      k = machine.preMem.queue[(i + 1) * -1]['instruction']
      p(('\tEntry %d:\t' % i)+'['+dissassemble(k)+']')
    else:
      p(('\tEntry %d:\t') %i)
  p('Post_MEM Queue:')
  if len(machine.postMem):
    p(('\tEntry %d:\t' % 0)+'['+dissassemble(machine.postMem.entry['instruction'])+']')
  else:
    p('\tEntry %d:\t' % 0)
  p() #print a blank line
  p('Registers')
  for i, v in enumerate(machine.registers):
    if(i % 8 == 0):
      out[0] += 'R%02d:' % i
    out[0] += '\t%d' % Word.convert32BitUnsignedToSigned(v)
    if(i % 8 == 7):
      p()
  p('Cache')
  for i, k in enumerate(machine.cache.sets):
    p('Set %d: LRU=%d' % (i, k.lru))
    for j, l in enumerate(k.entries):
      p('\tEntry %d:[(%d,%d,%d)<%s,%s>]' % (j, l.v, l.d, l.tag, bin(l.words[0]), bin(l.words[1])))
  p()
  dataAddr = findDataAddress(machine)
  p("Data")
  for i, instruction in enumerate(machine.memory.instructions[dataAddr:]):
    if(i % 8 == 0):
      out[0] += '%02d:' % (96 + (dataAddr + i) * 4)
    out[0] += '\t%d' % Word.convert32BitUnsignedToSigned(instruction)
    if(i % 8 == 7):
      p()
  p()
  file.write(out[0])
def dissassemble(word):
  instruction = Instruction(word)
  def SW(instruction):
    return "SW\tR" + str(instruction['rt']) + ", " + str(instruction['immed']) + "(R" + str(instruction['rs'])+")"
  def LW(instruction):
    return "LW\tR"+str(instruction['rt'])+ ", "+ str(instruction['immed'])+ "(R"+str(instruction['rs'])+")"
  def ADDI(instruction):
    return "ADDI\tR"+str(instruction['rt'])+ ", R"+str(instruction['rs'])+", #"+str(instruction['immed']) #Use rt for rd since this is an i type
  def BEQ(instruction):
    return "BEQ\tR"+str(instruction['rt'])+ ", R"+str(instruction['rs'])+", #",str(instruction['immed']) #Use rt for rd since this is an i type
  def J(instruction):
    return "J\t#"+ str(instruction['addr'] << 2)
  def BLTZ(instruction):
    return "BLTZ\tR"+str(instruction['rs'])+ ", #"+str(instruction['immed'] << 2)
  def MUL(instruction):
    return "MUL\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
  def BREAK(instruction):
    return 'BREAK'
  def MOVZ(instruction):
    return "MOVZ\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
  def INVALID(instruction):
    return 'Invalid Instruction'
  def SLL(instruction): #Could also be NOP, check included
    if(instruction.word & (2**31 - 1) == 0):
      return "NOP"
    else:
      return "SLL\tR"+str(instruction['rd'])+ ", R"+str(instruction['rt'])+", #"+str(instruction['sa'])
  def SRL(instruction):
    return "SRL\tR"+str(instruction['rd'])+ ", R"+str(instruction['rt'])+", #"+str(instruction['sa'])
  def ADD(instruction):
    return "ADD\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
  def SUB(instruction):
    return "SUB\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
  def AND(instruction):
    return "AND\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
  def OR(instruction) :
    return "OR\tR"+str(instruction['rd'])+ ", R"+str(instruction['rs'])+", R"+str(instruction['rt'])
  def JR(instruction) :
    return "JR\tR"+ str(instruction['rs'])
  op = instruction['op']
  if op == 0b100000 :# R Type, many cases
    func = instruction['func']
    if   func == 0b000000: return SLL(instruction)    # SLL or NOP
    elif func == 0b000010: return SRL(instruction)    # SRL
    elif func == 0b001000: return JR(instruction)    # JR
    elif func == 0b100000: return ADD(instruction)    # ADD
    elif func == 0b100010: return SUB(instruction)    # SUB
    elif func == 0b100100: return AND(instruction)  # AND
    elif func == 0b100101: return OR(instruction)    # OR
    elif func == 0b001010: return MOVZ(instruction) # MOVZ
    elif func == 0b001101: return BREAK(instruction)#BREAK
    else :           return INVALID(instruction)
  elif op == 0b111100: return MUL(instruction)    #MUL
  elif op == 0b100001: return BLTZ(instruction)    #BLTZ
  elif op == 0b100010: return J(instruction)        #J
  elif op == 0b100100: return BEQ(instruction)    #BEQ
  elif op == 0b101000: return ADDI(instruction)    #ADDI
  elif op == 0b100011: return LW(instruction)     #LW
  elif op == 0b101011: return SW(instruction)      #SW
  else:         return INVALID(instruction)
def findDataAddress(machine):
    for i, instruction in enumerate(machine.memory.instructions):
      instruction = Instruction(instruction)
      if instruction['op'] == 0b100000 and instruction['func'] == 0b001101: #BREAK statement
        return i + 1
    return -1