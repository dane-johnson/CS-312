from superscaler_sim.functional_unit import FunctionalUnit, UnitBuffer, READY, STALLED

from collections import deque

class PreALU(UnitBuffer): #standard FIFO queue
  def __init__(self, last, next):
    UnitBuffer.__init__(self, last, next)
    self.queue = deque()
  def __len__(self):
    return len(self.queue)
    
class PostALU(UnitBuffer): #one entry
  def __init__(self, last, next):
    UnitBuffer.__init__(self, last, next):
    self.entry = None
  def __len__(self):
    if entry == None: return 0
    return 1
    
class ALU(FunctionalUnit):
  def __init__(self, last, next):
    FunctionalUnit.__init__(self, last, next)
  
  def execute(self):
    if len(last) == 0:
      self.state = STALLED
    else:
      self.state = READY
    if self.state == STALLED:
      return
    curr = last.queue.pop() #should be a dictionary
    out = {} #blank dictionary
		op = curr['op']
    operands = curr['operands']
    out['dest'] = curr['dest']
    if op == 'add':
      out['data'] = operands[0] + operands[1] #add the operands
    elif op == 'sub':
      out['data'] = operands[0] - operands[1] #subtract the operands
    elif op == 'and':
      out['data'] = operands[0] & operands[1] #and the operands
    elif op == 'or':
      out['data'] = operands[0] | operands[1] #or the operands
    elif op == 'movz':
      if operand[0] == 0: #check and be sure equal to zero
        out['data'] = operands[1] #move the data
      else: #do not move the data, TODO
        pass
    elif op == 'sll':
      out['data'] = operands[0] << operands[1] #should be the shift amount
    elif op == 'srl':
      out['data'] = operands[0] >> operands[1] #should be the shift amount
    elif op == 'mul':
      out['data'] = operands[0] * operands[1] #multiply the operands
    
    next.entry = out #send the computed data to the post-alu buffer