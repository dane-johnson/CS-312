from superscaler_sim.functional_unit import FunctionalUnit, UnitBuffer, READY, STALLED

from collections import deque

class PreMEM(UnitBuffer): #standard FIFO queue
  def __init__(self):
    self.queue = deque()
  def __len__(self):
    return len(self.queue)

class PostMEM(UnitBuffer): #one entry output
  def __init__(self):
    self.entry = None
  def __len__(self):
    if entry == None: return 0
    return 1

class MEM(FunctionalUnit):
  def __init__(self, cache, preMem = None, postMem = None):
    FunctionalUnit.__init__(self)
    self.cache = cache
    self.preMem = preMem
    self.postMem = postMem
  
  def execute(self):
    pass #at this point, no idea