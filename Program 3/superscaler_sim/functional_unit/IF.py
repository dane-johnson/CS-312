from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED
from superscaler_sim.functional_unit.Issue import PreIssue

class IF (FunctionalUnit):
  def __init__(self, next, last):
    FunctionalUnit.__init__(self, next, last)
  def execute(self):
    if self.state == STALLED: return
    if next.size() == 4: return
    if next.size() == 3:
      #fetch a single instruction
      return
    #fetch 2 instructions