from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED

from collections import deque

class PreIssue(FunctionalUnit):
  def __init__(self, last, next):
    FunctionalUnit.__init__(self, last, next)
    self.buffer = deque()
  def execute(self):
    pass #do stuff here
  def size(self):
    return len(self.buffer)
 
class Issue(FunctionalUnit):
  def __init__(self, last, next):
    FunctionalUnit.__init__(self, last, next)
  
  def execute(self):
    pass #DO SOMETHING