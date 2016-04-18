READY = 0
STALLED = 1

class FunctionalUnit:
  def __init__(self, last, next):
    self.last = last
    self.next = next
    self.state = STALLED
  def execute(self):
    raise NotImplementedError()
    
class UnitBuffer:
  def __init__(self, last, next):
    self.last = last
    self.next = next
  def __len__(self):
    raise NotImplementedError()