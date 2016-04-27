from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED
from superscaler_sim.cache import CacheMissError
from superscaler_sim.word import Instruction

from pdb import set_trace as bp

class BranchError(Exception):
  def __init__(self):
    pass

class IF (FunctionalUnit):
  def __init__(self, cache, pc, registers, trigger, hazard ,preIssue = None):
    FunctionalUnit.__init__(self)
    self.cache = cache
    self.pc = pc
    self.registers = registers
    self.preIssue = preIssue
    self.trigger = trigger
    self.hazard = hazard
  def execute(self):
    if len(self.preIssue) == 4: return
    if len(self.preIssue) == 3:
      #fetch a single instruction
      try:
        self.fetch()
      except CacheMissError:
        self.state = STALLED
      except BranchError:
        return
      except Exception:
        raise
      finally:
        return
    #fetch 2 instructions
    try:
      self.fetch()
      self.fetch()
    except CacheMissError:
      self.state = STALLED
      return
    except BranchError:
      try:
        self.cache.getWord(self.pc[0])
      except CacheMissError:
        return
      return
    except TypeError:
      raise
  def fetch(self):
    word = self.cache.getWord(self.pc[0])
    #check if its valid
    if (word >> 31) <= 0:
      self.pc[0] += 4 #invalid
      return
    instruction = Instruction(word)
    op = instruction['op']
    #check if it is a branch
    if op == 0b100000 :# R Type, many cases
      func = instruction['func']
      if func == 0b000000:
        if instruction.word & (2**31 - 1) == 0: # NOP
          self.pc[0] += 4
        else:
          self.pc[0] += 4
      elif func == 0b001000:  # JR
        if len(self.hazard) == 0:
          self.pc[0] = instruction['rs']
          raise BranchError()
      elif func == 0b001101: #BREAK
        self.trigger[0] = True
        return
      else: self.pc[0] += 4
      self.preIssue.buffer.append(word)
    elif op == 0b100001:  #BLTZ
      if len(self.hazard) == 0:
        if self.registers[instruction['rs']] < 0:
          self.pc[0] += (instruction['immed'] << 2) + 4
        else:
          self.pc[0] += 4
        raise BranchError()
    elif op == 0b100010: #J
      self.pc[0] = instruction['addr'] << 2
      raise BranchError()
    elif op == 0b100100: #BEQ
      if len(self.hazard) == 0:
        if self.registers[instruction['rt']] == self.registers[instruction['rs']]:
          self.pc[0] = str(instruction['immed'])
        else:
          self.pc[0] += 4
        raise BranchError()
    else:
      self.preIssue.buffer.append(word)
      self.pc[0] += 4
    