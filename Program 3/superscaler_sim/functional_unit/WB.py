from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED

class WB(FunctionalUnit): 
  def __init__(self, registers, postMem = None, postAlu = None):
    FunctionalUnit.__init__(self)
    self.registers = registers
    self.postMem = postMem
    self.postAlu = postAlu
  def execute(self):
    if len(self.postAlu) == 0 and len(self.postMem) == 0: self.state = STALLED
    else: self.state = READY
    if self.state == READY:
      if len(self.postAlu) != 0:
        curr = self.postAlu.entry
        registers[curr['dest']] = curr['data']
      if len(self.postMem) != 0:
        curr = self.postMem.entry
        registers[curr['dest']] = curr['data']
      