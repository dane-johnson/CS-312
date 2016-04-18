from superscaler_sim.functional_unit import FunctionalUnit, UnitBuffer, READY, STALLED

from collections import deque

class PreIssue(UnitBuffer):
  def __init__(self, last, next):
    FunctionalUnit.__init__(self, last, next)
    self.buffer = deque()
  def __len__(self):
    return len(self.buffer)
 
class Issue(FunctionalUnit):
  def __init__(self, last, next):
    FunctionalUnit.__init__(self, last, next)
  
  def execute(self):
    pass #DO SOMETHING