from superscaler_sim.functional_unit import READY, STALLED
from superscaler_sim.functional_unit.IF import IF
from superscaler_sim.functional_unit.ALU import PreALU, ALU, PostALU
from superscaler_sim.functional_unit.Issue import PreIssue, Issue
from superscaler_sim.functional_unit.MEM import PreMEM, MEM, PostMEM
from superscaler_sim.cache import Cache

class Machine:
  def __init__(self, instructions):
    self.instructions = instructions
    self.pc = [96]
    self.registers = [0] * 32
    self.cache = Cache()
    self.cycleCount = 0
    self.shouldBreak = [False]
    
    self.preAlu = PreALU()
    self.postAlu = PostALU()
    self.alu = ALU(preAlu = self.preAlu, postAlu = self.postAlu)
    
    self.preMem = PreMEM()
    self.postMem = PostMEM()
    self.mem = MEM(cache = self.cache, preMem = self.preMem, postMem = self.postMem)
    
    self.preIssue = PreIssue()
    self.issue = Issue(registers = self.registers, preIssue = self.preIssue, preMem = self.preMem, preAlu = self.preAlu)
    
    self.wb = WB(registers = self.registers, preAlu = self.preAlu, postAlu = self.PostALU)
    
    self.fetch = IF(cache = self.cache, pc = self.pc, registers = self.registers, preIssue = self.preIssue, trigger = self.shouldBreak)
  def cycle(self):
	#execute in reverse order
    self.wb.execute()
    self.mem.execute()
    self.alu.execute()
    self.issue.execute()
    self.fetch.execute()
    cycleCount += 1 #increment counter
  def executeMix(self, f = None, *args): #f is a function to be run on the machine between each cycle
    self.cycleCount = 0
    while not self.shouldBreak[0]:
      if f != None:
        f(args)
      self.cycle()
