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
    pass #DO SOMETHING