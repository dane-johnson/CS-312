from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED
from superscaler_sim.functional_unit.Issue import PreIssue

class IF (FunctionalUnit):
  def __init__(self, next, last):
    FunctionalUnit.__init__(self, next, last)
  def execute(self):
    if self.state == STALLED: return
    if next.space == 0: return
    if next.space == 1:
      #fetch a single instruction
      return
    if next.space == 2:
      #fetch 2 instructions
      return