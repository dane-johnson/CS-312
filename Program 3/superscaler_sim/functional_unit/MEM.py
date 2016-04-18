from superscaler_sim.functional_unit import FunctionalUnit, UnitBuffer, READY, STALLED

from collections import deque

class PreMEM(UnitBuffer): #standard FIFO queue
  def __init__(self, next, last):
    UnitBuffer.__init__(self, next, last)
    self.queue = deque()
  def __len__(self):
    return len(self.queue)

class PostMEM(UnitBuffer): #one entry output
  def __init__(self, next, last):
    UnitBuffer.__init__(self, next, last)
    self.entry = None
  def __len__(self):
    if entry == None: return 0
    return 1

class MEM(FunctionalUnit):
  def __init__(self, next, last, cache):
    FunctionalUnit.__init__(self, next, last)
    self.cache = cache
  
  def execute(self):
    pass #at this point, no idea