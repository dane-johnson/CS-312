from superscaler_sim.functional_unit import FunctionalUnit, UnitBuffer, READY, STALLED
from superscaler_sim.cache import CacheMissError

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
    if self.entry == None: return 0
    return 1

class MEM(FunctionalUnit):
  def __init__(self, cache, hazard, preMem = None, postMem = None):
    FunctionalUnit.__init__(self)
    self.cache = cache
    self.preMem = preMem
    self.postMem = postMem
    self.hazard = hazard
  
  def execute(self):
    if len(self.preMem) == 0 and len(self.postMem) == 0:
      self.state = STALLED
    else:
      self.state = READY
    if self.state == READY:
      curr = self.preMem.queue[-1]
      op = curr['op']
      
      if op == 'sw':
        try:
          self.cache.storeWord(curr['addr'], curr['data'])
          self.preMem.queue.pop()
          self.hazard.complete(curr['instruction'])
        except CacheMissError:
          return #well get it next time
        except Exception:
          raise
      elif op == 'lw':
        try:
          dict = {}
          dict['instruction'] = curr['instruction'] #forward the instruction to the post memoryview
          dict['data'] = cache.getWord(curr['addr'])
          dict['dest'] = curr['dest']
          self.preMem.queue.pop()
          self.postMem.entry = dict
        except CacheMissError:
          return #don't pop, well get it next time
        except Exception:
          raise