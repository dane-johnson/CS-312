from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED
from superscaler_sim.cache import CacheMissError
from superscaler_sim.word import Instruction

from pdb import set_trace as bp

class BranchError(Exception):
  def __init__(self, tookBranch):
    self.tookBranch = tookBranch

class IF (FunctionalUnit):
  def __init__(self, cache, pc, registers, trigger, hazard ,preIssue = None, issue = None):
    FunctionalUnit.__init__(self)
    self.cache = cache
    self.pc = pc
    self.registers = registers
    self.preIssue = preIssue
    self.trigger = trigger
    self.hazard = hazard
    self.issue = issue
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
      twoLoad = False
      self.fetch()
      twoLoad = True
      self.fetch()
    except CacheMissError:
      self.state = STALLED
      return
    except BranchError as e:
      if (not e.tookBranch) and (not twoLoad) and (self.pc[0] >> 2) & 1 == 1:
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
        if self.hazard.checkBranch([instruction['rs']]):
          self.pc[0] = self.registers[instruction['rs']]
          raise BranchError(True)
      elif func == 0b001101: #BREAK
        self.trigger[0] = True
        return
      else: self.pc[0] += 4
      self.preIssue.buffer.append(word)
    elif op == 0b100001:  #BLTZ
      if self.hazard.checkBranch([instruction['rs']]):
        if self.registers[instruction['rs']] < 0:
          self.pc[0] += (instruction['immed'] << 2) + 4
          raise BranchError(True)
        else:
          self.pc[0] += 4
          raise BranchError(False)
    elif op == 0b100010: #J
      #bp()
      self.pc[0] = instruction['addr'] << 2
      raise BranchError(True)
    elif op == 0b100100: #BEQ
      if self.hazard.checkBranch([instruction['rs'], instruction['rt']]):
        if self.registers[instruction['rt']] == self.registers[instruction['rs']]:
          self.pc[0] = str(instruction['immed'])
          raise BranchError(True)
        else:
          self.pc[0] += 4
          raise BranchError(False)
    else:
      self.preIssue.buffer.append(word)
      self.hazard.noIssued.append(self.issue.buildInstruction(word))
      self.pc[0] += 4
    