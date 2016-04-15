READY = 0
STALLED = 1

class FunctionalUnit:
  def __init__(self, last, next):
    self.inputBuffer = []
    self.outputBuffer = []
    self.last = last
    self.next = next
    self.state = READY
  
  def execute(self):
    raise NotImplementedError