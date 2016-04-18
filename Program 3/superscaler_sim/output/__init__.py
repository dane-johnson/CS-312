def output(machine, file): #file should be an open, write textually file
  out = ''
  def p(x=''): out += x + '\n' #quick helper function
  p('-' * 20)
  p('Cycle %d:' % machine.cycle) #print the cycle
  p() #print a blank line
  p('Pre-Issue Buffer:')
  for i, k in enumerate(machine.preIssue.queue):
    p(('\tEntry %d:\t' % i)+dissassemble(k))
  p('Pre_ALU Queue:')
  for i, k in enumerate(machine.preALU.queue):
    p(('\tEntry %d:\t' % i)+dissassemble(k))
  p('Post_ALU Queue:')
  for i, k in enumerate(machine.postALU.queue):
    p(('\tEntry %d:\t' % i)+dissassemble(k))
  p('Pre_MEM Queue:')
  for i, k in enumerate(machine.preMEM.queue):
    p(('\tEntry %d:\t' % i)+dissassemble(k))
  p('Post_MEM Queue:')
  for i, k in enumerate(machine.postMEM.queue):
    p(('\tEntry %d:\t' % i)+dissassemble(k))
  p() #print a blank line
  p('Registers:')
  for i, v in enumerate(machine.registers):
	  if(i % 8 == 0):
			out += 'r%02d:' % i
		out += '\t%d' % v
		if(i % 8 == 7):
			p()
  for i, k in enumerate(machine.cache.sets):
    p('\tSet %d: LRU=%d' % i, k.lru)
    for i, k in enumerate(k.entries):
      p() #idk how cache works
  dataAddr = findDataAddress(machine)
  for i, instruction in enumerate(self.instructions[dataAddr:]):
		if(i % 8 == 0):
			out += '%02d:' % instruction.addr
		out += '\t%d' % instruction.word
		if(i % 8 == 7):
      p()
  file.write(out)
def findDataAddress(machine):
		for i, instruction in enumerate(machine.instructions):
			if instruction['op'] == 0b100000 and instruction['func'] == 0b001101: #BREAK statement
				return i + 1
		return len(instructions)