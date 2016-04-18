READY = 0
STALLED = 1

class FunctionalUnit:
  def __init__(self):
    self.state = STALLED
  def execute(self):
    raise NotImplementedError()
    
class UnitBuffer:
  def __len__(self):
    raise NotImplementedError()