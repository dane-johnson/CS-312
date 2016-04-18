from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED

class IF (FunctionalUnit):
  def __init__(self, next, last, cache, pc):
    FunctionalUnit.__init__(self, next, last)
    self.cache = cache
    self.pc = pc
  def execute(self):
    if self.state == STALLED: return
    if len(next) == 4: return
    if len(next) == 3:
      #fetch a single instruction
      return
    #fetch 2 instructions