from superscaler_sim.functional_unit import READY, STALLED
from superscaler_sim.functional_unit.IF import IF
from superscaler_sim.functional_unit.ALU import PreALU, ALU, PostALU
from superscaler_sim.functional_unit.Issue import PreIssue, Issue
from superscaler_sim.functional_unit.MEM import PreMEM, MEM, PostMEM
from superscaler_sim.functional_unit.WB import WB
from superscaler_sim.cache import Cache
from superscaler_sim.memory import Memory
from superscaler_sim.hazard import HazardUnit

from pdb import set_trace as bp

class Machine:
  def __init__(self, instructions):
    self.memory = Memory(instructions)
    self.pc = [96]
    self.hazard = HazardUnit()
    self.registers = [0] * 32
    self.cache = Cache(self.memory)
    self.cycleCount = 0
    self.shouldBreak = [False]
    self.preAlu = PreALU()
    self.postAlu = PostALU()
    self.alu = ALU(hazard = self.hazard, registers = self.registers, preAlu = self.preAlu, postAlu = self.postAlu)
    
    self.preMem = PreMEM()
    self.postMem = PostMEM()
    self.mem = MEM(cache = self.cache, registers = self.registers, hazard = self.hazard, preMem = self.preMem, postMem = self.postMem)
    
    self.preIssue = PreIssue()
    self.issue = Issue(registers = self.registers, hazard = self.hazard, preIssue = self.preIssue, preMem = self.preMem, preAlu = self.preAlu)
    
    self.wb = WB(registers = self.registers, hazard = self.hazard, postMem = self.postMem, postAlu = self.postAlu)
    
    self.fetch = IF(cache = self.cache, pc = self.pc, registers = self.registers, preIssue = self.preIssue, trigger = self.shouldBreak, hazard = self.hazard)
  def cycle(self):
  #execute in reverse order
    self.cache.memoryRead()
    self.wb.execute()
    self.mem.execute()
    self.alu.execute()
    self.issue.execute()
    self.fetch.execute()
    self.cycleCount += 1 #increment counter
  def executeMix(self, f = None, *args): #f is a function to be run on the machine between each cycle
    self.cycleCount = 0
    while not self.shouldBreak[0] or len(self.hazard) != 0:
      #bp()
      self.cycle()
      if self.shouldBreak[0] and len(self.hazard) == 0:
        self.cache.writeToMemory()
      if f != None:
        f(*args)