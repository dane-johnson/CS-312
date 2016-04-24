from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED
from superscaler_sim.cache import CacheMissException
from superscaler_sim.word import Instruction

class IF (FunctionalUnit):
  def __init__(self, cache, pc, registers, trigger,  preIssue = None):
    FunctionalUnit.__init__(self)
    self.cache = cache
    self.pc = pc
    self.registers = registers
    self.preIssue = preIssue
    self.trigger = trigger
  def execute(self):
    
    if self.state == STALLED:
      self.state = READY
      return
    if len(self.preIssue) == 4: return
    if len(self.preIssue) == 3:
      #fetch a single instruction
      try:
        self.fetch()
      except CacheMissException:
        self.state = STALLED
      finally:
        return
    #fetch 2 instructions
    try:
      self.fetch()
      self.fetch()
    except: CacheMissException:
      self.state = STALLED
    finally:
      return
  def fetch(self):
    word = cache.getWord(self.pc[0])
    #check if its valid
    if word >> 31 > 0:
      return #invalid instruction
    preIssue.append(word)
    instruction = Instruction(word, addr)
    op = instruction['op']
    #check if it is a branch
    if op == 0b100000 :# R Type, many cases
			func = instruction['func']
			if   func == 0b000000:
        if instruction.word & (2**31 - 1) == 0: return # NOP
			elif func == 0b001000: pass		# JR
			elif func == 0b001101: #BREAK
        self.trigger[0] = True
        return
		elif op == 0b100001: pass		#BLTZ
		elif op == 0b100010: #J
      self.pc[0] = instruction['addr'] << 2
      return
		elif op == 0b100100: pass		#BEQ
		else: 
      self.pc[0] += 4
    