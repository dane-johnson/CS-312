from superscaler_sim.functional_unit import FunctionalUnit, UnitBuffer, READY, STALLED

from collections import deque

class PreIssue(UnitBuffer):
  def __init__(self):
    self.buffer = deque()
  def __len__(self):
    return len(self.buffer)
 
class Issue(FunctionalUnit):
  def __init__(self, preIssue = None, preMem = None, preAlu = None):
    FunctionalUnit.__init__(self)
    self.preIssue = preIssue
    self.preMem = preMem
    self.preAlu = preAlu
  
  def execute(self):
    #set issued instructions = 0
    #go into a for loop that simply iterates twice
      #go into a for loop over the stack
        #if issued instructions == 2 > break outer loop
        #peek at the next instruction, determine op code, registers
        #Check for structural hazards, WAW hazards, WAR hazards, RAW hazards, previous sw issued 
      