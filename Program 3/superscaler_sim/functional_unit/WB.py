from superscaler_sim.functional_unit import FunctionalUnit, READY, STALLED

class WB(FunctionalUnit): 
  def __init__(self, registers, hazard, postMem = None, postAlu = None):
    FunctionalUnit.__init__(self)
    self.registers = registers
    self.postMem = postMem
    self.postAlu = postAlu
    self.hazard = hazard
  def execute(self):
    if len(self.postAlu) == 0 and len(self.postMem) == 0: self.state = STALLED
    else: self.state = READY
    if self.state == READY:
      if len(self.postAlu) != 0:
        curr = self.postAlu.entry
        self.postAlu.entry = None #clear the buffer
        self.registers[curr['dest']] = curr['data']
        self.hazard.complete(curr['instruction'])
      if len(self.postMem) != 0:
        curr = self.postMem.entry
        self.postMem = None #clear the buffer
        self.registers[curr['dest']] = curr['data']
        self.hazard.complete(curr['instruction'])