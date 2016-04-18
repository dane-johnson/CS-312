from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED

class IF (FunctionalUnit):
  def __init__(self, cache, pc, registers, preIssue = None):
    FunctionalUnit.__init__(self)
    self.cache = cache
    self.pc = pc
    self.registers = registers
    self.preIssue = preIssue
  def execute(self):
    if self.state == STALLED: return
    if len(self.preIssue) == 4: return
    if len(self.preIssue) == 3:
      #fetch a single instruction
      return
    #fetch 2 instructions